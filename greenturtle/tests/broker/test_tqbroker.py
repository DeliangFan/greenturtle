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

"""unittest for tq broker module"""

import unittest
from unittest import mock

import munch

from greenturtle.brokers import tqbroker
from greenturtle import exception
from greenturtle.util.notifier import fake


class TestSymbolConvert(unittest.TestCase):
    """unit tests for tqbroker.py"""

    def setUp(self):
        """setup the convert"""
        self.convert = tqbroker.SymbolConvert(None)

    def test_tq_symbol_2_db_symbol_success(self):
        """test tq_symbol_2_db_symbol success"""
        self.assertEqual(
            "pg2602",
            self.convert.tq_symbol_2_db_symbol("pg2602", "DCE"))
        self.assertEqual(
            "SP2601",
            self.convert.tq_symbol_2_db_symbol("sp2601", "SHFE"))
        self.assertEqual(
            "UR601",
            self.convert.tq_symbol_2_db_symbol("UR601", "CZCE"))
        self.assertEqual(
            "IF2504",
            self.convert.tq_symbol_2_db_symbol("IF2504", "CFFEX"))
        self.assertEqual(
            "SC2601",
            self.convert.tq_symbol_2_db_symbol("sc2601", "INE"))
        self.assertEqual(
            "SI2601",
            self.convert.tq_symbol_2_db_symbol("si2601", "GFEX"))

    def test_tq_symbol_2_db_symbol_failed(self):
        """test tq_symbol_2_db_symbol failed"""
        self.assertRaises(
            exception.ExchangeNotSupportedError,
            self.convert.tq_symbol_2_db_symbol,
            "pg2602", "xxx")
        self.assertRaises(
            exception.ExchangeNotSupportedError,
            self.convert.tq_symbol_2_db_symbol,
            "SP2601", "SHFaE")

    def test_db_symbol_2_tq_symbol_success(self):
        """test db_symbol_2_tq_symbol success"""
        self.assertEqual(
            "pg2602",
            self.convert.db_symbol_2_tq_symbol("pg2602", "DCE"))
        self.assertEqual(
            "sp2601",
            self.convert.db_symbol_2_tq_symbol("SP2601", "SHFE"))
        self.assertEqual(
            "UR601",
            self.convert.db_symbol_2_tq_symbol("UR601", "CZCE"))
        self.assertEqual(
            "IF2504",
            self.convert.db_symbol_2_tq_symbol("IF2504", "CFFEX"))
        self.assertEqual(
            "sc2601",
            self.convert.db_symbol_2_tq_symbol("SC2601", "INE"))
        self.assertEqual(
            "si2601",
            self.convert.db_symbol_2_tq_symbol("SI2601", "GFEX"))

    def test_db_symbol_2_tq_symbol_failed(self):
        """test db_symbol_2_tq_symbol failed"""
        self.assertRaises(
            exception.ExchangeNotSupportedError,
            self.convert.db_symbol_2_tq_symbol,
            "pg2602", "xxx")
        self.assertRaises(
            exception.ExchangeNotSupportedError,
            self.convert.db_symbol_2_tq_symbol,
            "SP2601", "SHFaE")


class TestTQBroker(unittest.TestCase):
    """unit tests for TQBroker class"""

    def get_valid_mock_conf(self):
        """get mock config"""
        conf = munch.Munch()
        conf.source = "AKShare"
        conf.country = "CN"
        conf.broker = munch.Munch()
        conf.broker.tq_broker = munch.Munch()
        conf.broker.tq_broker.tq_username = "username"
        conf.broker.tq_broker.tq_password = "password"
        return conf

    def get_mock_account(self):
        """get mock account"""
        account = munch.Munch({
            "balance": 10000,
            "available": 9000,
            "margin": 1000,
            "float_profit": 2000,
            "position_profit": 1500,
        })
        return account

    def get_mock_positions(self):
        """get mock position"""
        positions = {
            "CFFEX.IF2505": munch.Munch({
                "pos": 2,
                "pos_long": 2,
                "pos_short": 0,
                "open_cost_long": 200,
                "open_price_long": 202,
                "last_price": 101,
                "exchange_id": "CFFEX",
                "instrument_id": "IF2505",
                "float_profit_long": 2,
                "margin_long": 20,
            }),
            "CFFEX.IM2505": munch.Munch({
                "pos": -3,
                "pos_long": 0,
                "pos_short": 3,
                "open_cost_short": 300,
                "open_price_short": 100,
                "last_price": 99,
                "exchange_id": "CFFEX",
                "instrument_id": "IM2505",
                "float_profit_short": 3,
                "margin_short": 30,
            }),
        }

        return positions

    def mock_contract(self, name):
        """mock contract"""
        contract = munch.Munch({"variety": name})
        return contract

    def mock_contract_get_one_by_name_exchange(self, symbol, _):
        """mock contract_get_one_by_name_exchange"""
        if symbol.startswith("IF"):
            return self.mock_contract("IF")

        if symbol.startswith("IM"):
            return self.mock_contract("IM")

        raise NotImplementedError(symbol)

    def test_validate_config_success(self):
        """test validate_config success"""
        # test with simulate
        conf = self.get_valid_mock_conf()
        tqbroker.TQBroker.validate_config(conf)

        # test with simulate = False
        conf.broker.tq_broker.simulate = False
        conf.broker.tq_broker.broker_id = "broker_id"
        conf.broker.tq_broker.account_id = "account_id"
        conf.broker.tq_broker.password = "password"
        tqbroker.TQBroker.validate_config(conf)

    def test_validate_config_failed(self):
        """test validate_config success"""

        # test failed without broker in config
        conf = munch.Munch()
        self.assertRaises(AttributeError,
                          tqbroker.TQBroker.validate_config,
                          conf)

        # test failed without tq broker in config
        conf.broker = munch.Munch()
        self.assertRaises(AttributeError,
                          tqbroker.TQBroker.validate_config,
                          conf)

        # test failed without tq_username in config
        conf.broker.tq_broker = munch.Munch()
        self.assertRaises(ValueError,
                          tqbroker.TQBroker.validate_config,
                          conf)

        # test failed without broker_id in config
        conf.broker.tq_broker.simulate = False
        conf.broker.tq_broker.tq_username = "username"
        conf.broker.tq_broker.tq_password = "password"
        self.assertRaises(ValueError,
                          tqbroker.TQBroker.validate_config,
                          conf)

    def test_get_max_margin_ratio(self):
        """test get_max_margin_ratio"""
        # test with non strategy
        conf = munch.Munch()
        actual = tqbroker.TQBroker.get_max_margin_ratio(conf)
        self.assertEqual(0.3, actual)

        # test with non max_margin_ratio
        conf.strategy = munch.Munch()
        actual = tqbroker.TQBroker.get_max_margin_ratio(conf)
        self.assertEqual(0.3, actual)

        # test with max_margin_ratio
        conf.strategy.max_margin_ratio = 0.4
        actual = tqbroker.TQBroker.get_max_margin_ratio(conf)
        self.assertEqual(0.4, actual)

    def test_get_margin_ratio(self):
        """test get_margin_ratio"""
        conf = self.get_valid_mock_conf()
        notifier = fake.FakeNotifier()
        account = self.get_mock_account()
        mock_tq_qpi = mock.MagicMock()
        mock_tq_qpi.get_account = mock.MagicMock(return_value=account)

        b = tqbroker.TQBroker(conf, notifier)
        b.tq_api = mock_tq_qpi
        actual = b.get_margin_ratio()
        self.assertEqual(0.1, actual)

    def test_with_account_operations(self):
        """test with account operations"""
        conf = self.get_valid_mock_conf()
        notifier = fake.FakeNotifier()
        b = tqbroker.TQBroker(conf, notifier)

        # mock account
        account = self.get_mock_account()
        mock_tq_qpi = mock.MagicMock()
        mock_tq_qpi.get_account = mock.MagicMock(return_value=account)
        b.tq_api = mock_tq_qpi

        # test _get_account_from_tq
        # pylint:disable=protected-access
        account = b._get_account_from_tq()
        b.cash = account["available"]
        b.value = account["balance"]
        b.margin = account["margin"]

        self.assertEqual(9000, b.cash)
        self.assertEqual(9000, b.get_cash())
        self.assertEqual(10000, b.value)
        self.assertEqual(10000, b.get_value())
        self.assertEqual(10000, b.getvalue())

    def test_with_position_operations(self):
        """test with position operations"""

        conf = self.get_valid_mock_conf()
        notifier = fake.FakeNotifier()
        b = tqbroker.TQBroker(conf, notifier)

        # mock position
        mock_positions = self.get_mock_positions()
        mock_tq_qpi = mock.MagicMock()
        mock_tq_qpi.get_position = mock.MagicMock(return_value=mock_positions)

        # mock dbapi
        mock_dbapi = mock.MagicMock()
        mock_dbapi.contract_get_one_by_name_exchange = \
            self.mock_contract_get_one_by_name_exchange

        # mock the methods
        b.tq_api = mock_tq_qpi
        b.dbapi = mock_dbapi
        b.convert = tqbroker.SymbolConvert(mock_dbapi)

        # test _get_positions_from_tq
        # pylint:disable=protected-access
        positions = b._get_positions_from_tq()
        if_position = positions["CFFEX.IF2505"]
        im_position = positions["CFFEX.IM2505"]

        self.assertEqual(2, if_position["pos_long"])
        self.assertEqual(3, im_position["pos_short"])

        # test get_all_positions
        positions = b.get_all_positions()
        if_position = positions["IF"]
        im_position = positions["IM"]

        self.assertEqual(2, if_position.size)
        self.assertEqual(-3, im_position.size)

        # test getposition
        b.positions = positions
        mock_data = munch.Munch()
        # pylint:disable=protected-access
        mock_data._name = "IF"
        actual = b.getposition(mock_data)
        self.assertEqual(2, actual.size)

    def test_other_operations(self):
        """test other operations"""
        conf = self.get_valid_mock_conf()
        notifier = fake.FakeNotifier()
        b = tqbroker.TQBroker(conf, notifier)

        self.assertEqual(None, b.get_notification())
        self.assertRaises(NotImplementedError, b.submit, None)
        self.assertRaises(NotImplementedError, b.cancel, None)

    def test_validate_trading_parameters(self):
        """test _validate_trading_parameters"""
        # test success
        # pylint:disable=protected-access
        tqbroker.TQBroker._validate_trading_parameters(
            kwargs={"variety": "IF", "desired_size": 1})

        # test failed
        # pylint:disable=protected-access
        self.assertRaises(exception.VarietyNotFound,
                          tqbroker.TQBroker._validate_trading_parameters,
                          kwargs={"desired_size": 1})

        # pylint:disable=protected-access
        self.assertRaises(exception.DesiredSizeNotFound,
                          tqbroker.TQBroker._validate_trading_parameters,
                          kwargs={"variety": "IF"})
