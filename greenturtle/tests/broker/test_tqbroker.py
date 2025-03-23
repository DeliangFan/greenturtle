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
from greenturtle.util.logging import logging
from greenturtle.util.notifier import fake


logger = logging.get_logger()
logger.disabled = True


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


# pylint: disable=too-many-public-methods
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

    def get_mock_orders(self):
        """get mock orders"""
        orders = {
            "order1": munch.Munch({
                "exchange_id": "CFFEX",
                "instrument_id": "IF2505",
                "direction": "BUY",
                "offset": "OPEN",
                "volume_orign": 1,
                "limit_price": 10.1,
                "status": "ALIVE",
                "last_msg": "",
                "is_error": "",
            }),
            "order2": munch.Munch({
                "exchange_id": "CFFEX",
                "instrument_id": "IM2505",
                "direction": "BUY",
                "offset": "OPEN",
                "volume_orign": 2,
                "limit_price": 20.1,
                "status": "CLOSED",
                "last_msg": "",
                "is_error": "",
            }),
        }

        return orders

    def mock_get_quote(self, _):
        """mock get_quote"""
        quote = munch.Munch({
            "ask_price1": float(1.01),
            "bid_price1": float(1),
        })
        return quote

    def mock_get_quote_with_nan_price(self, _):
        """mock get_quote"""
        quote = munch.Munch({
            "ask_price1": float("nan"),
            "bid_price1": float("nan"),
        })
        return quote

    # pylint: disable=unused-argument
    def mock_continuous_contract_get_latest_by_variety_source_country(
            self, variety, *args):
        """
        mock the function
        continuous_contract_get_latest_by_variety_source_country
        """
        contract = munch.Munch({
            "variety": variety,
            "exchange": "CFFEX",
            "name": "IM2505",
        })
        return contract

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
        mock_tq_api = mock.MagicMock()
        mock_tq_api.get_account = mock.MagicMock(return_value=account)

        b = tqbroker.TQBroker(conf, notifier)
        b.tq_api = mock_tq_api
        actual = b.get_margin_ratio()
        self.assertEqual(0.1, actual)

    def test_with_account_operations(self):
        """test with account operations"""
        conf = self.get_valid_mock_conf()
        notifier = fake.FakeNotifier()
        b = tqbroker.TQBroker(conf, notifier)

        # mock account
        mock_account = self.get_mock_account()
        mock_tq_api = mock.MagicMock()
        mock_tq_api.get_account = mock.MagicMock(return_value=mock_account)
        b.tq_api = mock_tq_api

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
        mock_tq_api = mock.MagicMock()
        mock_tq_api.get_position = mock.MagicMock(return_value=mock_positions)

        # mock dbapi
        mock_dbapi = mock.MagicMock()
        mock_dbapi.contract_get_one_by_name_exchange = \
            self.mock_contract_get_one_by_name_exchange

        # mock the methods
        b.tq_api = mock_tq_api
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

        # test _get_position_from_tq_by_variety
        if_position = b._get_position_from_tq_by_variety("IF")
        im_position = b._get_position_from_tq_by_variety("IM")
        t_position = b._get_position_from_tq_by_variety("T")
        self.assertEqual(2, if_position["pos_long"])
        self.assertEqual(3, im_position["pos_short"])
        self.assertIsNone(t_position)

    def test_with_order_operations(self):
        """test with order operations"""

        conf = self.get_valid_mock_conf()
        notifier = fake.FakeNotifier()
        b = tqbroker.TQBroker(conf, notifier)

        # mock orders
        mock_orders = self.get_mock_orders()
        mock_tq_api = mock.MagicMock()
        mock_tq_api.get_order = mock.MagicMock(return_value=mock_orders)

        # mock dbapi
        mock_dbapi = mock.MagicMock()
        mock_dbapi.contract_get_one_by_name_exchange = \
            self.mock_contract_get_one_by_name_exchange

        # mock the methods
        b.tq_api = mock_tq_api
        b.dbapi = mock_dbapi
        b.convert = tqbroker.SymbolConvert(mock_dbapi)

        # test get_orders
        orders = b.get_orders()
        order1 = orders["order1"]
        order2 = orders["order2"]
        self.assertEqual(2, len(orders))
        self.assertEqual("IF2505", order1.instrument_id)
        self.assertEqual("IM2505", order2.instrument_id)

        # test get_orders_open
        orders = b.get_orders_open()
        self.assertEqual(1, len(orders))
        order = orders[0]
        self.assertEqual("IF2505", order.instrument_id)

        # test _has_open_order
        # pylint:disable=protected-access
        self.assertEqual(True, b._has_open_order("IF"))
        self.assertEqual(False, b._has_open_order("IM"))

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

    def test_buy_failed(self):
        """test buy failed"""

        conf = self.get_valid_mock_conf()
        notifier = fake.FakeNotifier()
        b = tqbroker.TQBroker(conf, notifier)

        # mock orders and positions
        mock_orders = self.get_mock_orders()
        mock_positions = self.get_mock_positions()

        mock_tq_api = mock.MagicMock()
        mock_tq_api.get_order = mock.MagicMock(return_value=mock_orders)
        mock_tq_api.get_position = mock.MagicMock(return_value=mock_positions)
        mock_tq_api.get_quote = self.mock_get_quote_with_nan_price

        # mock dbapi
        mock_dbapi = mock.MagicMock()
        mock_dbapi.contract_get_one_by_name_exchange = \
            self.mock_contract_get_one_by_name_exchange

        # mock the methods
        b.tq_api = mock_tq_api
        b.dbapi = mock_dbapi
        b.convert = tqbroker.SymbolConvert(mock_dbapi)

        # test buy failed without variety
        self.assertRaises(exception.VarietyNotFound,
                          b.buy,
                          None, None, 1)

        # test buy failed with open orders
        kwargs = {"variety": "IF", "desired_size": 1}
        b.buy(None, None, 1, **kwargs)

        # test buy failed with BuyOrSellSizeAbnormalError
        kwargs = {"variety": "IM", "desired_size": -1}
        self.assertRaises(exception.BuyOrSellSizeAbnormalError,
                          b.buy,
                          None, None, 1, **kwargs)

        # test buy failed with nan price
        kwargs = {"variety": "IM", "desired_size": -2}
        b.buy(None, None, 1, **kwargs)

    def test_buy_success(self):
        """test buy success"""

        conf = self.get_valid_mock_conf()
        notifier = fake.FakeNotifier()
        b = tqbroker.TQBroker(conf, notifier)
        b.max_margin_ratio = 0.3

        # mock account, orders and positions
        mock_account = self.get_mock_account()
        mock_positions = self.get_mock_positions()
        mock_orders = self.get_mock_orders()

        mock_tq_api = mock.MagicMock()
        mock_tq_api.get_order = mock.MagicMock(return_value=mock_orders)
        mock_tq_api.get_position = mock.MagicMock(return_value=mock_positions)
        mock_tq_api.get_account = mock.MagicMock(return_value=mock_account)

        mock_tq_api.get_quote = self.mock_get_quote

        # mock dbapi
        mock_dbapi = mock.MagicMock()
        mock_dbapi.contract_get_one_by_name_exchange = \
            self.mock_contract_get_one_by_name_exchange

        # mock the methods
        b.tq_api = mock_tq_api
        b.dbapi = mock_dbapi
        b.convert = tqbroker.SymbolConvert(mock_dbapi)

        # test buy failed with open orders
        kwargs = {"variety": "IM", "desired_size": -1}
        b.buy(None, None, 2, **kwargs)
        b.tq_api.assert_has_calls(
            [
                mock.call.insert_order(symbol='CFFEX.IM2505',
                                       direction='BUY',
                                       offset='CLOSE',
                                       limit_price=1.01,
                                       volume=2),
            ],
            any_order=True)

    def test_sell_failed(self):
        """test sell failed"""

        notifier = fake.FakeNotifier()
        conf = self.get_valid_mock_conf()
        b = tqbroker.TQBroker(conf, notifier)

        # mock orders and positions
        mock_positions = self.get_mock_positions()
        mock_orders = self.get_mock_orders()

        mock_tq_api = mock.MagicMock()
        mock_tq_api.get_order = mock.MagicMock(return_value=mock_orders)
        mock_tq_api.get_position = mock.MagicMock(return_value=mock_positions)
        mock_tq_api.get_quote = self.mock_get_quote_with_nan_price

        # mock dbapi
        mock_dbapi = mock.MagicMock()
        mock_dbapi.contract_get_one_by_name_exchange = \
            self.mock_contract_get_one_by_name_exchange
        mock_dbapi.continuous_contract_get_latest_by_variety_source_country = \
            self.mock_continuous_contract_get_latest_by_variety_source_country

        # mock the methods
        b.tq_api = mock_tq_api
        b.dbapi = mock_dbapi
        b.convert = tqbroker.SymbolConvert(mock_dbapi)

        # test buy failed without variety
        self.assertRaises(exception.VarietyNotFound,
                          b.buy,
                          None, None, 1)

        # test buy failed with open orders
        kwargs = {"variety": "IF", "desired_size": 1}
        b.sell(None, None, 1, **kwargs)

        # test buy failed with BuyOrSellSizeAbnormalError
        kwargs = {"variety": "IM", "desired_size": -1}
        self.assertRaises(exception.BuyOrSellSizeAbnormalError,
                          b.sell,
                          None, None, 1, **kwargs)

        # test buy failed with nan price
        kwargs = {"variety": "IM", "desired_size": -4}
        b.sell(None, None, 1, **kwargs)

    def test_sell_success(self):
        """test sell success"""

        conf = self.get_valid_mock_conf()
        notifier = fake.FakeNotifier()
        b = tqbroker.TQBroker(conf, notifier)
        b.max_margin_ratio = 0.3

        # mock account, orders and positions
        mock_account = self.get_mock_account()
        mock_orders = self.get_mock_orders()
        mock_positions = self.get_mock_positions()

        mock_tq_api = mock.MagicMock()
        mock_tq_api.get_order = mock.MagicMock(return_value=mock_orders)
        mock_tq_api.get_position = mock.MagicMock(return_value=mock_positions)
        mock_tq_api.get_account = mock.MagicMock(return_value=mock_account)

        mock_tq_api.get_quote = self.mock_get_quote

        # mock dbapi
        mock_dbapi = mock.MagicMock()
        mock_dbapi.contract_get_one_by_name_exchange = \
            self.mock_contract_get_one_by_name_exchange
        mock_dbapi.continuous_contract_get_latest_by_variety_source_country = \
            self.mock_continuous_contract_get_latest_by_variety_source_country

        # mock the methods
        b.tq_api = mock_tq_api
        b.dbapi = mock_dbapi
        b.convert = tqbroker.SymbolConvert(mock_dbapi)

        # test buy failed with open orders
        kwargs = {"variety": "IM", "desired_size": -4}
        b.sell(None, None, 1, **kwargs)
        b.tq_api.assert_has_calls(
            [
                mock.call.insert_order(symbol='CFFEX.IM2505',
                                       direction='SELL',
                                       offset='OPEN',
                                       limit_price=1,
                                       volume=1),
            ],
            any_order=True)

    def test_rolling_failed(self):
        """test rolling failed"""
        conf = self.get_valid_mock_conf()
        notifier = fake.FakeNotifier()
        b = tqbroker.TQBroker(conf, notifier)
        b.max_margin_ratio = 0.3

        # mock account, orders and positions
        mock_account = self.get_mock_account()
        mock_orders = self.get_mock_orders()
        mock_positions = self.get_mock_positions()

        mock_tq_api = mock.MagicMock()
        mock_tq_api.get_order = mock.MagicMock(return_value=mock_orders)
        mock_tq_api.get_position = mock.MagicMock(return_value={})
        mock_tq_api.get_account = mock.MagicMock(return_value=mock_account)

        mock_tq_api.get_quote = self.mock_get_quote

        # mock dbapi
        mock_dbapi = mock.MagicMock()
        mock_dbapi.contract_get_one_by_name_exchange = \
            self.mock_contract_get_one_by_name_exchange
        mock_dbapi.continuous_contract_get_latest_by_variety_source_country = \
            self.mock_continuous_contract_get_latest_by_variety_source_country

        # mock the methods
        b.tq_api = mock_tq_api
        b.dbapi = mock_dbapi
        b.convert = tqbroker.SymbolConvert(mock_dbapi)

        # test rolling failed with non position
        b.rolling()

        # test rolling failed with same symbol
        mock_tq_api.get_position = mock.MagicMock(return_value=mock_positions)
        b.rolling()

    def test_rolling_success(self):
        """test rolling success"""
        conf = self.get_valid_mock_conf()
        notifier = fake.FakeNotifier()
        b = tqbroker.TQBroker(conf, notifier)
        b.max_margin_ratio = 0.3

        # mock account, orders and positions
        mock_account = self.get_mock_account()
        mock_orders = self.get_mock_orders()
        mock_positions = self.get_mock_positions()
        tmp = mock_positions.pop("CFFEX.IM2505")
        tmp["instrument_id"] = "IM2503"
        mock_positions["CFFEX.IM2503"] = tmp

        mock_tq_api = mock.MagicMock()
        mock_tq_api.get_order = mock.MagicMock(return_value=mock_orders)
        mock_tq_api.get_position = mock.MagicMock(return_value=mock_positions)
        mock_tq_api.get_account = mock.MagicMock(return_value=mock_account)

        mock_tq_api.get_quote = self.mock_get_quote

        # mock dbapi
        mock_dbapi = mock.MagicMock()
        mock_dbapi.contract_get_one_by_name_exchange = \
            self.mock_contract_get_one_by_name_exchange
        mock_dbapi.continuous_contract_get_latest_by_variety_source_country = \
            self.mock_continuous_contract_get_latest_by_variety_source_country

        # mock the methods
        b.tq_api = mock_tq_api
        b.dbapi = mock_dbapi
        b.convert = tqbroker.SymbolConvert(mock_dbapi)

        # test rolling failed with non position
        b.rolling()

        b.tq_api.assert_has_calls(
            [
                mock.call.insert_order(symbol='CFFEX.IM2505',
                                       direction='SELL',
                                       offset='OPEN',
                                       limit_price=1.0,
                                       volume=3),
                mock.call.insert_order(symbol='CFFEX.IM2503',
                                       direction='BUY',
                                       offset='CLOSE',
                                       limit_price=1.01,
                                       volume=3),
            ],
            any_order=True)
