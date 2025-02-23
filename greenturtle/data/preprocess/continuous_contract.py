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

from greenturtle.constants.future import types
from greenturtle.data import transform
from greenturtle.data import validation
from greenturtle import exception
from greenturtle.util.logging import logging

logger = logging.get_logger()


class ContinuousContract:
    """ContinuousContract is used to generate continuous contract."""
    def __init__(self, variety, source, country, dbapi):
        self.variety = variety
        self.source = source
        self.country = country
        self.dbapi = dbapi

    def get_all_contracts(self):
        """get all the contract according to the variety."""
        getter = None
        if self.source == types.AKSHARE and self.country == types.CN:
            getter = self.dbapi.contract_get_all_by_variety_from_akshare_cn
        elif self.source == types.CSI and self.country == types.US:
            getter = self.dbapi.contract_get_all_by_variety_from_us_cn

        if getter is None:
            raise exception.SourceCountryNotSupportedError

        contracts = getter(self.variety)
        logger.info("get all %s contracts success", self.variety)

        return contracts

    def generate(self):
        """
        generate continuous contracts and write to database.
        """

        # 1. get all contracts and build a sorted date index
        contracts = self.get_all_contracts()
        dates = self.get_sorted_dates(contracts)
        continuous_contracts = {}

        # 2. select the main contract for every date
        logger.info("start build %s continuous contracts", self.variety)
        for date in dates:
            contract = self.get_main_contract(date)
            contract = transform.contract_model_2_continuous_contract_model(
                contract)
            continuous_contracts[date] = contract
        logger.info("build %s continuous contracts success", self.variety)

        # 3. compute the adjust factor
        self.compute_adjust_factor(dates, continuous_contracts)
        logger.info("compute %s adjustment factor success", self.variety)

        # 4. refine other attributes
        self.refine_other_attributes(dates, continuous_contracts)
        logger.info("refine %s other attributes", self.variety)

        # 5. validate the contract order
        self.validate(dates, continuous_contracts)
        msg = f"validate {self.variety} continuous contracts order success"
        logger.info(msg)

        # 6. write to database
        self.write_to_db(continuous_contracts)
        msg = f"write {self.variety} continuos contract to database success"
        logger.info(msg)

    def compute_adjust_factor(self, dates, continuous_contracts):
        """compute adjustment factor."""
        prev = continuous_contracts[dates[0]]
        for date in dates[1:]:
            now = continuous_contracts[date]

            # compute the adjust factor
            if now.name != prev.name:
                tmp = self.dbapi.contract_get_by_constraint(
                    date, prev.name, self.variety, self.source, self.country
                )
                now.adjust_factor = now.close / tmp.close

            prev = now

    def validate(self, dates, continuous_contracts):
        """validate continuous contracts."""
        # validate the contract order
        self.validate_order(dates, continuous_contracts)

        # validate the price field
        for v in continuous_contracts.values():
            validation.validate_price(v.open, v.high, v.low, v.close)

        # validate the nan

    @staticmethod
    def validate_order(dates, continuous_contracts):
        """validate the contract order"""
        if len(dates):
            return

        sets = set()
        prev = continuous_contracts[dates[0]].name
        sets.add(prev)

        for date in dates[1:]:
            contract = continuous_contracts[date]
            if contract.name == prev:
                continue
            # raise exception for not continuous contract
            if contract.name in sets:
                raise exception.ContinuousContractOrderAbnormalError

            sets.add(contract.name)

    def get_main_contract(self, date):
        """
        get the main contract according to volume, open interest or expire
        TODO: add support for expire
        """
        return self.get_main_contract_by_volume(date)

    def get_main_contract_by_volume(self, date):
        """get the main contract according to volume"""
        getter = self.dbapi.contract_get_all_by_date_variety_source_country
        contracts = getter(date, self.variety, self.source, self.country)
        contracts.sort(key=lambda x: x.volume, reverse=True)

        if len(contracts) == 0:
            raise exception.ContractNotFound

        return contracts[0]

    def get_main_contract_by_open_interest(self, date):
        """get the main contract according to open interest"""
        getter = self.dbapi.contract_get_all_by_date_variety_source_country

        contracts = getter(date, self.variety, self.source, self.country)
        contracts.sort(key=lambda x: x.open_interest, reverse=True)

        if len(contracts) == 0:
            raise exception.ContractNotFound

        return contracts[0]

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

    def refine_other_attributes(self, dates, continuous_contracts):
        """
        refine other attributes.

        add total_volume, total_open_interest
        """

        getter = self.dbapi.contract_get_all_by_date_variety_source_country

        for date in dates:
            contracts = getter(date, self.variety, self.source, self.country)
            total_volume = self._get_total_volume(contracts)
            total_open_interest = self._get_total_open_interest(contracts)
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

    def write_to_db(self, continuous_contracts):
        """write to database."""
        for c in continuous_contracts.values():
            self.dbapi.continuous_contract_create(c.date,
                                                  c.name,
                                                  c.variety,
                                                  c.source,
                                                  c.country,
                                                  c.exchange,
                                                  c.group,
                                                  c.to_dict())
