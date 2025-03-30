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

"""unittest for delta syncer"""

import datetime
import unittest
from unittest import mock

import munch

from greenturtle.constants import types
from greenturtle.data.deltasyncer import delta_syncer
from greenturtle.db import models
from greenturtle import exception
from greenturtle.util import calendar


class TestDeltaSyncer(unittest.TestCase):
    """unittest for delta syncer"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.decision_date = calendar.decision_regard_date()

    def setUp(self):
        """set up for expire"""
        self.expire = datetime.datetime.combine(
            self.decision_date, datetime.datetime.min.time())

    # pylint:disable=unused-argument
    def mock_contract_get_all_by_variety_source_country_since_date(
            self, variety, *args, **kwargs):
        """mock contract_get_all_by_variety_source_country_since_date"""
        contract = models.Contract(
            variety=variety,
            expire=self.expire,
        )
        return [contract]

    # pylint:disable=unused-argument
    def mock_contract_get_by_constraint_with_none(self, *args, **kwargs):
        """mock contract_get_by_constraint"""
        return None

    # pylint:disable=unused-argument
    def mock_contract_get_by_constraint(self, date, *args):
        """mock contract_get_by_constraint"""
        contracts = [models.Contract(date=datetime.datetime(2025, 4, 2))]

        for contract in contracts:
            if contract.date == date:
                return contract

        return None

    # pylint:disable=unused-argument
    def mock_contract_get_all_by_name_source_country(self, symbol, *args):
        """mock contract_get_all_by_name_source_country"""
        contracts = [
            models.Contract(
                expire=datetime.datetime(2025, 4, 2),
                name="IF2505",
            ),
        ]

        ret = []
        for contract in contracts:
            if contract.name == symbol:
                ret.append(contract)

        return ret

    def test_has_delta_contracts_synced_with_true(self):
        """test has_delta_contracts_synced"""
        conf = munch.Munch({"source": "akshare", "country": "CN"})
        mock_dbapi = mock.MagicMock()
        mock_dbapi.contract_get_all_by_variety_source_country_since_date = \
            self.mock_contract_get_all_by_variety_source_country_since_date
        d = delta_syncer.DeltaSyncer(conf, mock_dbapi)

        self.assertEqual(True, d.has_delta_contracts_synced())

    def test_has_delta_contracts_synced_with_false(self):
        """test has_delta_contracts_synced"""
        conf = munch.Munch({"source": "akshare", "country": "CN"})
        mock_dbapi = mock.MagicMock()
        mock_dbapi.contract_get_all_by_variety_source_country_since_date = \
            self.mock_contract_get_all_by_variety_source_country_since_date
        mock_dbapi.contract_get_by_constraint = \
            self.mock_contract_get_by_constraint_with_none
        d = delta_syncer.DeltaSyncer(conf, mock_dbapi)

        self.expire = self.expire + datetime.timedelta(days=10)
        self.assertEqual(False, d.has_delta_contracts_synced())

    def test_write_contracts_to_database(self):
        """test _write_contracts_to_database"""
        conf = munch.Munch({"source": "akshare", "country": "CN"})
        mock_dbapi = mock.MagicMock()
        mock_dbapi.contract_get_by_constraint = \
            self.mock_contract_get_by_constraint

        d = delta_syncer.DeltaSyncer(conf, mock_dbapi)
        contracts = [
            {
                types.DATE: datetime.datetime(2025,  4,  1),
                types.NAME: "IF2505",
                types.VARIETY: "IF",
                types.COUNTRY: "CN",
                types.SOURCE: "akshare",
                types.EXCHANGE: types.CFFEX,
                types.GROUP: "indices",
            },
            {
                types.DATE: datetime.datetime(2025,  4,  2),
                types.NAME: "IF2505",
                types.VARIETY: "IF",
                types.COUNTRY: "CN",
                types.SOURCE: "akshare",
                types.EXCHANGE: types.CFFEX,
                types.GROUP: "indices",
            }
        ]

        # pylint:disable=protected-access
        actual = d._write_contracts_to_database(contracts)
        self.assertEqual(1, actual)

    def test_validate_contracts(self):
        """test _validate_contracts"""

        # pylint:disable=protected-access
        func = delta_syncer.DeltaSyncer._validate_contracts

        # test validate failed with DataPriceInvalidTypeError
        contract = {"open": 100, "high": 102, "low": 98, "close": 0}
        self.assertRaises(exception.DataPriceInvalidTypeError,
                          func,
                          [contract])

        # test validate failed with DataPriceInvalidTypeError
        contract = {"open": 0, "high": 0, "low": 0, "close": None}
        self.assertRaises(exception.DataPriceInvalidTypeError,
                          func,
                          [contract])

        # test validate failed with DataPriceInvalidTypeError
        contract = {
            "open": 100,
            "high": 102,
            "low": 98,
            "close": 99,
        }
        self.assertRaises(exception.DataInvalidExpireError,
                          func,
                          [contract])

        # test validate failed with DataPriceInvalidTypeError
        contract = {
            "open": 100,
            "high": 102,
            "low": 98,
            "close": 99,
            "expire": None,
        }
        self.assertRaises(exception.DataInvalidExpireError,
                          func,
                          [contract])

        # test validate success
        contract = {
            "open": 100,
            "high": 102,
            "low": 98,
            "close": 99,
            "expire": datetime.datetime.now(),
        }
        func([contract])

    def test_set_symbol(self):
        """test _set_symbol"""
        conf = munch.Munch({"source": "akshare", "country": "CN"})
        mock_dbapi = mock.MagicMock()
        mock_dbapi.contract_get_all_by_name_source_country = \
            self.mock_contract_get_all_by_name_source_country

        d = delta_syncer.DeltaSyncer(conf, mock_dbapi)

        # test _set_symbol success with matching symbol names
        symbol = "IF2505"
        symbols_expire = {"IF2505": datetime.datetime(2025, 4, 1)}
        contract = {}
        # pylint:disable=protected-access
        d._set_symbol(contract, symbol, symbols_expire)
        self.assertEqual(datetime.datetime(2025, 4, 1), contract[types.EXPIRE])

        # test _set_symbol success with matching lower symbol names
        symbol = "IF2505"
        symbols_expire = {"if2505": datetime.datetime(2025, 4, 1)}
        contract = {}
        # pylint:disable=protected-access
        d._set_symbol(contract, symbol, symbols_expire)
        self.assertEqual(datetime.datetime(2025, 4, 1), contract[types.EXPIRE])

        # test _set_symbol success with matching upper symbol names
        symbol = "if2505"
        symbols_expire = {"IF2505": datetime.datetime(2025, 4, 1)}
        contract = {}
        # pylint:disable=protected-access
        d._set_symbol(contract, symbol, symbols_expire)
        self.assertEqual(datetime.datetime(2025, 4, 1), contract[types.EXPIRE])

        # test _set_symbol success with no matching names
        symbol = "IF2505"
        symbols_expire = {}
        contract = {}
        # pylint:disable=protected-access
        d._set_symbol(contract, symbol, symbols_expire)
        self.assertEqual(datetime.datetime(2025, 4, 2), contract[types.EXPIRE])

        # test _set_symbol failed with
        symbol = "IM2505"
        symbols_expire = {}
        contract = {}
        self.assertRaises(exception.DataInvalidExpireError,
                          d._set_symbol,
                          contract, symbol, symbols_expire)
