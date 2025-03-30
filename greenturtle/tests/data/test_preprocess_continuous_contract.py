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

"""unittest for continuous_contract.py"""

import datetime
import unittest
from unittest import mock

from greenturtle.db import models
from greenturtle.data.preprocess import continuous_contract
from greenturtle import exception


class TestContinuousContract(unittest.TestCase):
    """test cases for ContinuousContract"""

    # pylint:disable=unused-argument
    def mock_contract_get_all_by_variety_source_country(self, *args):
        """mock contract_get_all_by_variety_source_country"""
        contracts = [models.Contract(name="IF2505")]
        return contracts

    # pylint:disable=unused-argument
    def mock_contract_get_all_by_date_variety_source_country(
            self, date, *args):
        """mock contract_get_all_by_date_variety_source_country"""
        contracts = [
            models.Contract(name="IF2505",
                            date=datetime.datetime(2025, 3, 25),
                            expire=datetime.datetime(2025, 5, 12),
                            volume=1,
                            open_interest=100000),
            models.Contract(name="IF2503",
                            date=datetime.datetime(2025, 3, 26),
                            expire=datetime.datetime(2025, 3, 12),
                            volume=2,
                            open_interest=100000),
            models.Contract(name="IF2505",
                            date=datetime.datetime(2025, 3, 26),
                            expire=datetime.datetime(2025, 5, 12),
                            volume=3,
                            open_interest=100),
            models.Contract(name="IF2506",
                            date=datetime.datetime(2025, 3, 26),
                            expire=datetime.datetime(2025, 6, 12),
                            volume=4,
                            open_interest=10000),
            models.Contract(name="IF2507",
                            date=datetime.datetime(2025, 3, 26),
                            expire=datetime.datetime(2025, 7, 12),
                            volume=5,
                            open_interest=1000),
        ]

        ret = []
        for contract in contracts:
            if contract.date == date:
                ret.append(contract)

        return ret

    def mock_contract_get_by_constraint(self, date, name, *args):
        """test contract_get_by_constraint"""
        contracts = [
            models.Contract(
                name="IF2503",
                date=datetime.datetime(2025, 3, 25),
                close=100,
            ),
            models.Contract(
                name="IF2503",
                date=datetime.datetime(2025, 3, 26),
                close=101,
            ),
            models.Contract(
                name="IF2503",
                date=datetime.datetime(2025, 3, 27),
                close=102,
            ),
            models.Contract(
                name="IF2505",
                date=datetime.datetime(2025, 3, 25),
                close=200,
            ),
            models.Contract(
                name="IF2505",
                date=datetime.datetime(2025, 3, 26),
                close=202,
            ),
            models.Contract(
                name="IF2505",
                date=datetime.datetime(2025, 3, 27),
                close=204,
            ),
        ]

        for contract in contracts:
            if contract.date == date and contract.name == name:
                return contract

        return None

    def mock_continuous_contract_create(self, *args):
        """mock continuous_contract_create"""

    def mock_continuous_contract_get_by_constraint(self, date, *args):
        """mock continuous_contract_get_by_constraint"""
        contracts = [
            models.Contract(
                name="IF2503",
                date=datetime.datetime(2025, 3, 25),
                close=100,
            ),
            models.Contract(
                name="IF2503",
                date=datetime.datetime(2025, 3, 26),
                close=101,
            ),
        ]

        ret = []
        for contract in contracts:
            if contract.date == date:
                ret.append(contract)

        return ret

    def test_get_sorted_dates(self):
        """test get_sorted_dates"""
        c1 = models.Contract(date=datetime.datetime(2025, 3, 26))
        c2 = models.Contract(date=datetime.datetime(2025, 3, 24))
        c3 = models.Contract(date=datetime.datetime(2025, 3, 25))

        func = continuous_contract.ContinuousContract.get_sorted_dates
        actual = func([c1, c2, c3])
        expect = [
            datetime.datetime(2025, 3, 24),
            datetime.datetime(2025, 3, 25),
            datetime.datetime(2025, 3, 26),
        ]
        self.assertEqual(expect, actual)

    def test_get_all_contracts(self):
        """test get_all_contracts"""
        # test get all contracts failed
        c = continuous_contract.ContinuousContract(variety="IF",
                                                   source="unknown",
                                                   country="unknown",
                                                   dbapi=None)
        self.assertRaises(exception.SourceCountryNotSupportedError,
                          c.get_all_contracts)

        mock_dbapi = mock.MagicMock()
        mock_dbapi.contract_get_all_by_variety_source_country = \
            self.mock_contract_get_all_by_variety_source_country

        c = continuous_contract.ContinuousContract(variety="IF",
                                                   source="akshare",
                                                   country="CN",
                                                   dbapi=mock_dbapi)
        contracts = c.get_all_contracts()
        self.assertEqual(1, len(contracts))
        self.assertEqual("IF2505", contracts[0].name)

    def test_get_main_contract_by_open_interest(self):
        """
        test get_main_contract_by_open_interest
        test get_main_contract
        """
        mock_dbapi = mock.MagicMock()
        mock_dbapi.contract_get_all_by_date_variety_source_country = \
            self.mock_contract_get_all_by_date_variety_source_country
        c = continuous_contract.ContinuousContract(variety="IF",
                                                   source="akshare",
                                                   country="CN",
                                                   dbapi=mock_dbapi)

        # test failed with contract not found
        self.assertRaises(exception.ContractNotFound,
                          c.get_main_contract_by_open_interest,
                          datetime.datetime(2025, 3, 27), None)

        self.assertRaises(exception.ContractNotFound,
                          c.get_main_contract,
                          datetime.datetime(2025, 3, 27), None)

        # test success with None pre_contract
        actual = c.get_main_contract_by_open_interest(
            datetime.datetime(2025, 3, 26), None)
        self.assertEqual("IF2506", actual.name)

        actual = c.get_main_contract(
            datetime.datetime(2025, 3, 26), None)
        self.assertEqual("IF2506", actual.name)

        # test success with pre_contract
        pre_contract = models.Contract(expire=datetime.datetime(2025, 6, 14))
        actual = c.get_main_contract_by_open_interest(
            datetime.datetime(2025, 3, 26), pre_contract)
        self.assertEqual("IF2507", actual.name)

        actual = c.get_main_contract(
            datetime.datetime(2025, 3, 26), pre_contract)
        self.assertEqual("IF2507", actual.name)

    def test_build_continuous_contract(self):
        """test build_continuous_contract"""
        mock_dbapi = mock.MagicMock()
        mock_dbapi.contract_get_all_by_date_variety_source_country = \
            self.mock_contract_get_all_by_date_variety_source_country

        c = continuous_contract.ContinuousContract(variety="IF",
                                                   source="akshare",
                                                   country="CN",
                                                   dbapi=mock_dbapi)

        date0 = datetime.datetime(2025, 3, 25)
        date1 = datetime.datetime(2025, 3, 26)
        dates = [date0, date1]

        actual = c.build_continuous_contract(dates, None)
        self.assertEqual(2, len(actual))
        self.assertEqual("IF2505", actual[date0].name)
        self.assertEqual("IF2506", actual[date1].name)

    def test_get_total_volume(self):
        """test _get_total_volume"""
        contracts = [
            models.Contract(volume=10),
            models.Contract(volume=12),
        ]

        # pylint:disable=protected-access
        actual = continuous_contract.ContinuousContract._get_total_volume(
            contracts=contracts)

        self.assertEqual(22, actual)

    def test_get_total_open_interest(self):
        """test _get_total_open_interest"""
        contracts = [
            models.Contract(open_interest=66),
            models.Contract(open_interest=10),
        ]

        # pylint:disable=protected-access
        func = continuous_contract.ContinuousContract._get_total_open_interest
        actual = func(contracts=contracts)

        self.assertEqual(76, actual)

    def test_compute_total_volume_and_open_interest(self):
        """test compute_total_volume_and_open_interest"""
        mock_dbapi = mock.MagicMock()
        mock_dbapi.contract_get_all_by_date_variety_source_country = \
            self.mock_contract_get_all_by_date_variety_source_country

        c = continuous_contract.ContinuousContract(variety="IF",
                                                   source="akshare",
                                                   country="CN",
                                                   dbapi=mock_dbapi)

        date0 = datetime.datetime(2025, 3, 25)
        date1 = datetime.datetime(2025, 3, 26)
        dates = [date0, date1]
        contracts = {
            date0: models.ContinuousContract(),
            date1: models.ContinuousContract(),
        }

        c.compute_total_volume_and_open_interest(dates, contracts)
        c0 = contracts[date0]
        self.assertEqual(1, c0.total_volume)
        self.assertEqual(100000, c0.total_open_interest)

        c1 = contracts[date1]
        self.assertEqual(111100, c1.total_open_interest)
        self.assertEqual(14, c1.total_volume)

    def test_compute_adjust_factor(self):
        """test compute_adjust_factor"""
        mock_dbapi = mock.MagicMock()
        mock_dbapi.contract_get_by_constraint = \
            self.mock_contract_get_by_constraint

        c = continuous_contract.ContinuousContract(variety="IF",
                                                   source="akshare",
                                                   country="CN",
                                                   dbapi=mock_dbapi)

        date0 = datetime.datetime(2025, 3, 25)
        date1 = datetime.datetime(2025, 3, 26)
        date2 = datetime.datetime(2025, 3, 27)
        dates = [date0, date1, date2]
        contracts = {
            date0: models.ContinuousContract(
                name="IF2503",
                adjust_factor=1.0,
                close=100,
            ),
            date1: models.ContinuousContract(
                name="IF2505",
                adjust_factor=1.0,
                close=202,
            ),
            date2: models.ContinuousContract(
                name="IF2505",
                close=204,
                adjust_factor=1.0),
        }

        c.compute_adjust_factor(dates, contracts)
        self.assertEqual(1, contracts[date0].adjust_factor)
        self.assertEqual(2, contracts[date1].adjust_factor)
        self.assertEqual(1, contracts[date2].adjust_factor)

    def test_validate_order(self):
        """test validate_order"""
        c = continuous_contract.ContinuousContract(variety="IF",
                                                   source="akshare",
                                                   country="CN",
                                                   dbapi=None)

        date0 = datetime.datetime(2025, 3, 26)
        date1 = datetime.datetime(2025, 3, 27)
        date2 = datetime.datetime(2025, 3, 28)
        dates = [date0, date1, date2]

        # test validate order success
        contracts = {
            date0: models.ContinuousContract(name="IF2503"),
            date1: models.ContinuousContract(name="IF2505"),
            date2: models.ContinuousContract(name="IF2505"),
        }
        # pylint:disable=protected-access
        self.assertEqual(True, c._validate_order(dates, contracts))

        # test validate order failed
        contracts = {
            date0: models.ContinuousContract(name="IF2503"),
            date1: models.ContinuousContract(name="IF2505"),
            date2: models.ContinuousContract(name="IF2503"),
        }
        # pylint:disable=protected-access
        self.assertEqual(False, c._validate_order(dates, contracts))

    def test_validate_and_fix_price(self):
        """test validate_and_fix_price"""

        c = continuous_contract.ContinuousContract(variety="IF",
                                                   source="akshare",
                                                   country="CN",
                                                   dbapi=None)

        date0 = datetime.datetime(2025, 3, 26)
        date1 = datetime.datetime(2025, 3, 27)

        # test validate high/low price abnormal for offline
        dates = [date0]
        contracts = {
            date0: models.ContinuousContract(name="IF2503",
                                             open=10,
                                             high=9,
                                             low=9,
                                             close=9),
        }
        # pylint:disable=protected-access
        c._validate_and_fix_price(dates, contracts)
        self.assertEqual(10, contracts[date0].high)

        # test validate high/low price abnormal for online
        contracts = {
            date0: models.ContinuousContract(name="IF2503",
                                             open=10,
                                             high=9,
                                             low=9,
                                             close=9),
        }
        # pylint:disable=protected-access
        self.assertRaises(exception.DataPriceHighAbnormalError,
                          c._validate_and_fix_price,
                          dates, contracts, True)

        # test validate DataPriceNonPositiveError abnormal for offline
        dates = [date0, date1]
        contracts = {
            date0: models.ContinuousContract(name="IF2503",
                                             open=10,
                                             high=11,
                                             low=9,
                                             close=9),
            date1: models.ContinuousContract(name="IF2503",
                                             open=10,
                                             high=11,
                                             low=-1,
                                             close=9),
        }
        # pylint:disable=protected-access
        c._validate_and_fix_price(dates, contracts)
        self.assertEqual(9, contracts[date1].low)

        # test validate DataPriceNonPositiveError abnormal for online
        dates = [date0, date1]
        contracts = {
            date0: models.ContinuousContract(name="IF2503",
                                             open=10,
                                             high=11,
                                             low=9,
                                             close=9),
            date1: models.ContinuousContract(name="IF2503",
                                             open=10,
                                             high=11,
                                             low=-1,
                                             close=9),
        }
        # pylint:disable=protected-access
        self.assertRaises(exception.DataPriceNonPositiveError,
                          c._validate_and_fix_price,
                          dates, contracts, True)

    def test_validate_prices_between_days(self):
        """test _validate_prices_between_days"""

        c = continuous_contract.ContinuousContract(variety="IF",
                                                   source="akshare",
                                                   country="CN",
                                                   dbapi=None)

        date0 = datetime.datetime(2025, 3, 26)
        date1 = datetime.datetime(2025, 3, 27)
        dates = [date0, date1]

        contracts = {
            date0: models.ContinuousContract(name="IF2503",
                                             open=10,
                                             high=11,
                                             low=9,
                                             close=9),
            date1: models.ContinuousContract(name="IF2503",
                                             open=10,
                                             high=11,
                                             low=10,
                                             close=9),
        }

        # validate prices between days success
        # pylint:disable=protected-access
        c._validate_prices_between_days(dates, contracts)

        # validate prices between days failed
        contracts = {
            date0: models.ContinuousContract(name="IF2503",
                                             open=10,
                                             high=11,
                                             low=9,
                                             close=9),
            date1: models.ContinuousContract(name="IF2503",
                                             open=20,
                                             high=22,
                                             low=20,
                                             close=19),
        }
        # pylint:disable=protected-access
        self.assertRaises(exception.DataPriceExceedDailyLimitError,
                          c._validate_prices_between_days,
                          dates, contracts)

    def test_validate_volume_and_open_interest(self):
        """test _validate_volume_and_open_interest"""

        c = continuous_contract.ContinuousContract(variety="IF",
                                                   source="akshare",
                                                   country="CN",
                                                   dbapi=None)

        date0 = datetime.datetime(2025, 3, 26)
        dates = [date0]

        # test validate failed with low volume and open interest
        contracts = {
            date0: models.ContinuousContract(name="IF2503",
                                             volume=10,
                                             open_interest=10),
        }
        # pylint:disable=protected-access
        self.assertEqual(
            False,
            c._validate_volume_and_open_interest(dates, contracts))

        # test validate failed with low volume and open interest
        contracts = {
            date0: models.ContinuousContract(name="IF2503",
                                             volume=10000,
                                             open_interest=10000),
        }
        # pylint:disable=protected-access
        self.assertEqual(
            True,
            c._validate_volume_and_open_interest(dates, contracts))

    def test_write_to_db(self):
        """test write_to_db"""

        mock_dbapi = mock.MagicMock()
        mock_dbapi.continuous_contract_get_by_constraint = \
            self.mock_continuous_contract_get_by_constraint
        mock_dbapi.continuous_contract_create = \
            self.mock_continuous_contract_create

        c = continuous_contract.ContinuousContract(variety="IF",
                                                   source="akshare",
                                                   country="CN",
                                                   dbapi=mock_dbapi)

        date0 = datetime.datetime(2025, 3, 26)
        date1 = datetime.datetime(2025, 3, 27)
        date2 = datetime.datetime(2025, 3, 28)

        # test validate order success
        continuous_contracts = {
            date0: models.ContinuousContract(name="IF2503", date=date0),
            date1: models.ContinuousContract(name="IF2505", date=date1),
            date2: models.ContinuousContract(name="IF2507", date=date2),
        }

        self.assertEqual(2, c.write_to_db(continuous_contracts))
