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

from backtrader import feed
from backtrader import date2num

from greenturtle.constants import types
from greenturtle.db import api


class ContinuousContractDB(feed.DataBase):
    """datafeed from continuous contract table in database"""

    params = (
        ("db_conf", None),
        (types.VARIETY, None),
        (types.SOURCE, types.AKSHARE),
        (types.COUNTRY, types.CN),
        (types.START_DATE, None),
        (types.END_DATE, None),
    )

    @staticmethod
    def _get_sort_dates(continuous_contracts):
        """get sort date from the continuous contracts."""

        date_set = set()
        for continuous_contract in continuous_contracts:
            if continuous_contract.date not in date_set:
                date_set.add(continuous_contract.date)

        dates = list(date_set)
        dates.sort(reverse=True)
        return dates

    @staticmethod
    def _get_continuous_contracts_dict(continuous_contracts):
        """get continuous contracts dict."""
        d = {}
        for c in continuous_contracts:
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
            adjust_factor = adjust_factor * continuous_contract.adjust_factor

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

        return True
