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
