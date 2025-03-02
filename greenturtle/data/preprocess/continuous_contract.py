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

"""continuous contract."""

import datetime

from greenturtle.constants import types
from greenturtle.constants import varieties
from greenturtle.data import transform
from greenturtle.data import validation
from greenturtle import exception
from greenturtle.util.logging import logging


ROLLING_INTERVAL = 15
logger = logging.get_logger()


class ContinuousContract:
    """ContinuousContract is used to generate continuous contract."""
    def __init__(self, variety, source, country, dbapi):
        self.variety = variety
        self.source = source
        self.country = country
        self.dbapi = dbapi

    def generate(self):
        """
        generate continuous contracts and write to database.
        """
        # get all contracts and build a sorted date index
        contracts = self.get_all_contracts()
        dates = self.get_sorted_dates(contracts)

        # select the main contract for every date
        continuous_contracts = self.build_continuous_contract(dates)

        # compute the adjust factor
        self.compute_adjust_factor(dates, continuous_contracts)
        logger.info("compute %s adjustment factor success", self.variety)

        # compute total volume and total open interest
        self.compute_total_volume_and_open_interest(dates,
                                                    continuous_contracts)
        logger.info("compute %s total volume, open interest success",
                    self.variety)

        # validate the contract order
        self.validate_and_fix(dates, continuous_contracts)
        msg = f"validate {self.variety} continuous contracts success"
        logger.info(msg)

        # write to database
        self.write_to_db(continuous_contracts)
        msg = f"write {self.variety} continuous contract to database success"
        logger.info(msg)

    @staticmethod
    def get_sorted_dates(contracts):
        """get date set."""
        date_set = set()
        for contract in contracts:
            if contract.date not in date_set:
                date_set.add(contract.date)

        dates = list(date_set)
        dates.sort()

        return dates

    def build_continuous_contract(self, dates, prev_contract=None):
        """get continuous contract from main contract."""
        logger.info("start build %s continuous contracts", self.variety)

        continuous_contracts = {}
        for date in dates:
            contract = self.get_main_contract(date, prev_contract)
            contract = transform.contract_model_2_continuous_contract_model(
                contract)
            continuous_contracts[date] = contract
            prev_contract = contract

        logger.info("build %s continuous contracts success", self.variety)

        return continuous_contracts

    def get_all_contracts(self):
        """get all the contract according to the variety."""
        support = False
        if self.source == types.AKSHARE and self.country == types.CN:
            support = True
        elif self.source == types.CSI and self.country == types.US:
            support = True

        if not support:
            raise exception.SourceCountryNotSupportedError

        contracts = self.dbapi.contract_get_all_by_variety_source_country(
            self.variety, self.source, self.country)

        logger.info("get all %s contracts success", self.variety)

        return contracts

    def get_main_contract(self, date, prev_contract):
        """
        get the main contract according to volume, open interest or expire
        """
        return self.get_main_contract_by_open_interest(date, prev_contract)

    def get_main_contract_by_volume(self, date):
        """
        get the main contract according to volume
        according to the benchmark, the volume is always a bad metrics.
        """
        getter = self.dbapi.contract_get_all_by_date_variety_source_country
        contracts = getter(date, self.variety, self.source, self.country)
        contracts.sort(key=lambda x: x.volume, reverse=True)

        if len(contracts) == 0:
            raise exception.ContractNotFound

        return contracts[0]

    def get_main_contract_by_open_interest(self, date, prev_contract):
        """
        1. get the main contract according to open interest
        2. make sure the contract is ROLLING_INTERVAL before expired
        3. will not switch back to early contract
        """
        getter = self.dbapi.contract_get_all_by_date_variety_source_country
        contracts = getter(date, self.variety, self.source, self.country)

        contracts.sort(key=lambda x: x.open_interest, reverse=True)
        if len(contracts) == 0:
            raise exception.ContractNotFound

        for contract in contracts:
            expire = contract.expire
            if not expire:
                raise exception.DataInvalidExpireError

            date = contract.date
            if date + datetime.timedelta(days=ROLLING_INTERVAL) < expire:
                if prev_contract is None:
                    return contract
                if expire >= prev_contract.expire:
                    return contract

        raise exception.ContractNotFound

    def compute_adjust_factor(self, dates, continuous_contracts):
        """compute adjustment factor."""
        prev = continuous_contracts[dates[0]]
        for date in dates[1:]:
            now = continuous_contracts[date]
            # compute the adjust factor
            if now.name == prev.name:
                prev = now
                continue

            # adjust according today's close price
            tmp = self.dbapi.contract_get_by_constraint(
                date, prev.name, self.variety, self.source, self.country)
            if tmp is not None:
                factor = now.close / tmp.close
                now.adjust_factor = factor
                msg = f"{date} {self.variety} adjust factor: {factor}"
                logger.info(msg)
                prev = now
                continue

            # adjust according to yesterday's close price, anyway, it's
            # work around for some corner cases
            tmp = self.dbapi.contract_get_by_constraint(
                prev.date, now.name, self.variety, self.source, self.country)
            if tmp is not None:
                factor = tmp.close / prev.close
                now.adjust_factor = factor
                msg = f"{date} {self.variety} adjust factor: {factor}"
                logger.info(msg)
                prev = now
            else:
                msg = f"failed compute {self.variety} {date} adjust factor"
                logger.error(msg)
                raise exception.ContractNotFound

    def compute_total_volume_and_open_interest(self,
                                               dates,
                                               continuous_contracts):
        """compute total volume and total open interest"""
        getter = self.dbapi.contract_get_all_by_date_variety_source_country

        for date in dates:
            # get the contract with the same date
            contracts = getter(date, self.variety, self.source, self.country)
            total_volume = self._get_total_volume(contracts)
            total_open_interest = self._get_total_open_interest(contracts)

            # set the total_volume and total_open_interest
            current = continuous_contracts[date]
            current.total_volume = total_volume
            current.total_open_interest = total_open_interest

    @staticmethod
    def _get_total_volume(contracts):
        """
        compute total volume according to the contracts on the same date.
        """
        total_volume = 0
        for contract in contracts:
            total_volume += contract.volume
        return total_volume

    @staticmethod
    def _get_total_open_interest(contracts):
        """
        compute total open interest according to the contracts on the same
        date.
        """
        total_open_interest = 0
        for contract in contracts:
            total_open_interest += contract.open_interest
        return total_open_interest

    def validate_and_fix(self, dates, continuous_contracts, online=False):
        """validate continuous contracts."""
        # validate the contract order
        self._validate_order(dates, continuous_contracts)

        # validate and fix the price field
        self._validate_and_fix_price(dates, continuous_contracts, online)

        # validate price between days
        self._validate_prices_between_days(dates, continuous_contracts)

        # pay attention to the low volume and open interest
        self._validate_volume_and_open_interest(dates, continuous_contracts)

    def _validate_order(self, dates, continuous_contracts):
        """validate the contract order"""
        if len(dates) == 0:
            return

        sets = set()
        prev = continuous_contracts[dates[0]]
        sets.add(prev.name)

        for date in dates[1:]:
            now = continuous_contracts[date]
            if now.name == prev.name:
                continue
            # raise exception for not continuous contract
            if now.name in sets:
                msg = f"{self.variety} contract {date} bad order"
                logger.error(msg)

            sets.add(now.name)
            prev = now

    def _validate_and_fix_price(self,
                                dates,
                                continuous_contracts,
                                online=False):
        """validate and fix the contract price."""
        prev = None
        for date in dates:
            contract = continuous_contracts[date]
            try:
                # validate the price
                validation.validate_price(
                    contract.open,
                    contract.high,
                    contract.low,
                    contract.close
                )
            except (
                    exception.DataPriceLowAbnormalError,
                    exception.DataPriceHighAbnormalError
            ) as exc:
                if online:
                    logger.error("panic, would not fix for online trading")
                    raise exc

                # deal with data price high/low abnormal error
                msg = f"validate price {self.variety} {date} failed, fix it"
                logger.error(msg)
                # fix the data
                contract.low = min(
                    contract.open,
                    contract.high,
                    contract.low,
                    contract.close)
                contract.high = max(
                    contract.open,
                    contract.high,
                    contract.low,
                    contract.close)
            except (
                    exception.DataPriceInvalidTypeError,
                    exception.DataPriceNonPositiveError
            ) as exc:
                if online:
                    logger.error("panic, would not fix for online trading")
                    raise exc

                # deal with data price invalid type and non-positive error
                msg = f"validate price type {self.variety} {date} failed" + \
                      ", fix it"
                logger.error(msg)
                # fix the data
                if prev is not None:
                    contract.open = prev.open
                    contract.high = prev.high
                    contract.low = prev.low
                    contract.close = prev.close
                else:
                    # raise the exception since failed to deal with it
                    msg = f"failed to fix price type {self.variety} {date}"
                    logger.error(msg)
                    raise exc

            prev = contract

    @staticmethod
    def _validate_prices_between_days(dates, continuous_contracts):
        """validate prices between days."""
        pre = continuous_contracts[dates[0]]
        for date in dates[1:]:
            cur = continuous_contracts[date]
            validation.validate_price_daily_limit(pre.close, cur.close)
            validation.validate_price_daily_limit(
                cur.high,
                cur.low,
                2 * varieties.DEFAULT_CN_DAILY_LIMIT)

    def _validate_volume_and_open_interest(self, dates, continuous_contracts):
        """
        validate the contract volume and open interest with low value
        - volume < 1000
        - open interest < 1500
        """
        for date in dates:
            contract = continuous_contracts[date]
            if contract.volume < 1000:
                logger.warning(
                    "%s %s low volume: %d",
                    self.variety,
                    date,
                    contract.volume)
            if contract.open_interest < 1500:
                logger.warning(
                    "%s %s low open interest: %d",
                    self.variety,
                    date,
                    contract.open_interest)

    def write_to_db(self, continuous_contracts):
        """write to database."""
        count = 0
        for c in continuous_contracts.values():
            # only insert if not exist
            found = self.dbapi.continuous_contract_get_by_constraint(
                c.date, c.variety, c.source, c.country)
            if found:
                logger.info("%s %s already exist, skip", c.variety, c.date)
                continue

            count += 1
            self.dbapi.continuous_contract_create(
                c.date, c.name, c.variety, c.source, c.country,
                c.exchange, c.group, c.to_dict())
            logger.info("insert %s %s to db success", c.variety, c.date)

        logger.info("insert %d row for %s to db success", count, self.variety)


class DeltaContinuousContract(ContinuousContract):
    """
    DeltaContinuousContract is used to generate delta continuous
    contract, especially in online serving scenario.
    """

    def generate(self):
        """
        generate delta continuous contracts and write to database.
        """
        func = self.dbapi.continuous_contract_get_latest_by_variety_source_country  # noqa: E501
        continuous_contract = func(self.variety, self.source, self.country)

        if continuous_contract is None:
            raise exception.ContinuousContractNotFound
            # logger.warning("no continuous contract found, generate full")
            # self.generate_full()
            # return

        # get all contracts and build a sorted date index
        contracts = self.get_all_contracts_since_date(
            continuous_contract.date)
        if len(contracts) == 0:
            logger.warning("no contract found since %s for %s",
                           continuous_contract.date, self.variety)
            return

        dates = self.get_sorted_dates(contracts)

        # select the main contract for every date
        continuous_contracts = self.build_continuous_contract(
            dates, continuous_contract)

        # compute the adjust factor
        self.compute_adjust_factor(dates, continuous_contracts)
        logger.info("compute %s adjustment factor success for delta",
                    self.variety)

        # compute total volume and total open interest
        self.compute_total_volume_and_open_interest(dates,
                                                    continuous_contracts)
        logger.info(
            "compute %s total volume, open interest success for delta",
            self.variety)

        # validate the contract order
        self.validate_and_fix(dates, continuous_contracts, online=True)
        msg = f"validate {self.variety} delta continuous contracts success"
        logger.info(msg)

        # write to database
        self.write_to_db(continuous_contracts)
        msg = f"write {self.variety} delta continuous contract to db success"
        logger.info(msg)

    def get_all_contracts_since_date(self, date):
        """get all contracts since date"""
        f = self.dbapi.contract_get_all_by_variety_source_country_since_date
        contracts = f(self.variety, self.source, self.country, date)
        logger.info("get %s contracts since %s success", self.variety, date)
        return contracts
