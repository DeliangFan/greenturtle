# Copyright (c) 2025 GreenTurtle
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""datafeed from database"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import copy
from datetime import datetime

from backtrader import feed
from backtrader import date2num

from greenturtle.constants import types
from greenturtle.constants import varieties
from greenturtle.data import validation
from greenturtle.db import api
from greenturtle import exception
from greenturtle.util import calendar
from greenturtle.util.logging import logging


logger = logging.get_logger()


class ContinuousContractDB(feed.DataBase):
    """datafeed from continuous contract table in database"""

    lines = types.CONTINUOUS_LINES

    params = (
        ("db_conf", None),
        (types.VARIETY, None),
        (types.SOURCE, types.AKSHARE),
        (types.COUNTRY, types.CN),
        (types.START_DATE, None),
        (types.END_DATE, None),
        ("padding", False),
        ("plot", False),
    )

    @staticmethod
    def _get_sort_dates(continuous_contracts, date_format=False):
        """get sort date from the continuous contracts."""

        date_set = set()
        for continuous_contract in continuous_contracts:
            date = continuous_contract.date
            if date_format:
                date = date.date()

            if date not in date_set:
                date_set.add(date)

        dates = list(date_set)
        dates.sort(reverse=True)
        return dates

    @staticmethod
    def _get_continuous_contracts_dict(continuous_contracts,
                                       date_format=False):
        """get continuous contracts dict."""
        d = {}
        for c in continuous_contracts:
            if date_format:
                d[c.date.date()] = c
            else:
                d[c.date] = c
        return d

    def adjust_price(self, continuous_contracts):
        """adjust price according to the adjust factor."""
        dates = self._get_sort_dates(continuous_contracts)
        continuous_contracts_dict = self._get_continuous_contracts_dict(
            continuous_contracts)

        adjust_factor = 1
        for date in dates:
            continuous_contract = continuous_contracts_dict[date]
            continuous_contract.open *= adjust_factor
            continuous_contract.high *= adjust_factor
            continuous_contract.low *= adjust_factor
            continuous_contract.close *= adjust_factor
            continuous_contract.pre_settle *= adjust_factor
            continuous_contract.settle *= adjust_factor
            adjust_factor = adjust_factor * continuous_contract.adjust_factor

    @staticmethod
    def _validate_trading_dates(dates, trading_dates):
        """validate trading dates"""
        for date in dates:
            if date not in trading_dates:
                logger.error("%s not in trading dates", date)
                raise exception.ValidateTradingDayError

    def align_and_padding(self, continuous_contracts):
        """
        1. align with the start date and end date
        2. padding if the date is missing in trading dates
        """

        dates = self._get_sort_dates(continuous_contracts, date_format=True)
        continuous_contracts_dict = self._get_continuous_contracts_dict(
            continuous_contracts, date_format=True)

        # pylint: disable=no-member
        trading_dates = calendar.get_cn_trading_days(
            self.p.start_date.date(),
            self.p.end_date.date())

        self._validate_trading_dates(dates, trading_dates)

        # padding from old to new
        prev = None
        for trading_date in trading_dates:
            if trading_date not in continuous_contracts_dict:
                if prev is not None:
                    # deep copy the previous and set the attributes
                    # valid = 0 means it's faking data, should not be used
                    # for trading
                    padding = copy.deepcopy(prev)
                    padding.date = datetime.combine(trading_date,
                                                    datetime.min.time())
                    padding.adjust_factor = 1
                    padding.valid = 0

                    # add padding to continuous_contracts and
                    # continuous_contracts_dict
                    continuous_contracts_dict[trading_date] = padding
                    continuous_contracts.append(padding)
                    logger.warning("padding %s %s from %s",
                                   self.p.variety,
                                   padding.date,
                                   prev.date)
                    # set prev
                    prev = padding
            else:
                prev = continuous_contracts_dict[trading_date]

        # padding from new to old
        trading_dates.sort(reverse=True)
        prev = None
        for trading_date in trading_dates:
            if trading_date not in continuous_contracts_dict:
                if prev is not None:
                    # deep copy the previous and set the attributes
                    # valid = 0 means it's faking data, should not be used
                    # for trading
                    padding = copy.deepcopy(prev)
                    padding.date = datetime.combine(trading_date,
                                                    datetime.min.time())
                    padding.valid = 0
                    # add padding to continuous_contracts and
                    # continuous_contracts_dict
                    padding.adjust_factor = 1
                    continuous_contracts_dict[trading_date] = padding
                    continuous_contracts.append(padding)
                    # set prev
                    prev = padding
            else:
                prev = continuous_contracts_dict[trading_date]

    @staticmethod
    def validate(continuous_contracts):
        """validate before feed"""
        pre = None
        for cur in continuous_contracts:
            if pre is None:
                pre = cur
                continue
            # pylint: disable=R0801
            validation.validate_price_daily_limit(pre.close, cur.close)
            validation.validate_price_daily_limit(
                cur.high,
                cur.low,
                2 * varieties.DEFAULT_CN_DAILY_LIMIT)

            pre = cur

    def start(self):
        """start the datafeed"""
        super().start()

        # pylint: disable=no-member, line-too-long
        dbapi = api.DBAPI(self.p.db_conf)
        getter = dbapi.continuous_contract_get_by_variety_source_country_start_end_date  # noqa: E501

        # pylint: disable=no-member
        continuous_contracts = getter(self.p.variety,
                                      self.p.source,
                                      self.p.country,
                                      start_date=self.p.start_date,
                                      end_date=self.p.end_date)

        self.adjust_price(continuous_contracts)

        logger.info("%s actual data length %d",
                    self.p.variety,
                    len(continuous_contracts))

        # do align and padding
        if self.p.padding:
            self.align_and_padding(continuous_contracts)
            logger.info("after align and padding, %s data length %d",
                        self.p.variety,
                        len(continuous_contracts))

        # sort the continuous contracts
        continuous_contracts.sort(key=lambda x: x.date)

        # validation before feed
        self.validate(continuous_contracts)

        # pylint: disable=attribute-defined-outside-init
        self.iter = iter(continuous_contracts)

    def _load(self):
        """load data every once"""
        try:
            continuous_contract = next(self.iter)
        except StopIteration:
            return False

        # pylint: disable=no-member
        self.l.datetime[0] = date2num(continuous_contract.date)
        self.l.open[0] = continuous_contract.open
        self.l.high[0] = continuous_contract.high
        self.l.low[0] = continuous_contract.low
        self.l.close[0] = continuous_contract.close
        self.l.volume[0] = continuous_contract.volume
        self.l.valid[0] = 1
        if hasattr(continuous_contract, "valid"):
            self.l.valid[0] = continuous_contract.valid

        return True
