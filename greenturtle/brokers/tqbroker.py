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

"""tq broker"""

import collections
import math
import time

import backtrader as bt
import tqsdk

from greenturtle.constants import types
from greenturtle.db import api
from greenturtle import exception
from greenturtle.util.logging import logging


logger = logging.get_logger()
# order status
ORDER_ALIVE = "ALIVE"


class SymbolConvert:
    """
    convert symbol between greenturtle and tq broker, for more details,
    please refer to https://doc.shinnytech.com/tqsdk/latest/usage/mddatas.html

    1. the exchange code are same between tq and db
            DEC  SHFE  CZCE  CFFEX  INE  GFEX
        db  DEC  SHFE  CZCE  CFFEX  INE  GFEX
        tq  DEC  SHFE  CZCE  CFFEX  INE  GFEX

    2. the contract name are different between exchanges
            DEC    SHFE   CZCE   CFFEX  INE    GFEX
        db  lower  upper  upper  upper  upper  upper
        tq  lower  lower  upper  upper  lower  lower

      for example
            DEC         SHFE         CZCE        CFFEX         INE         GFEX
        db  pg2602      SP2601       UR601       IF2504        SC2601      SI2601
        tq  DEC.pg2602  SHFE.sp2601  CZCE.UR601  CFFEX.IF2504  INE.sc2601  GFEX.si2601
    """  # noqa E501

    def __init__(self, dbapi):
        self.dbapi = dbapi

    @staticmethod
    def tq_symbol_2_db_symbol(symbol, exchange):
        """tq symbol to db symbol"""
        if exchange in [types.SHFE, types.INE, types.GFEX]:
            return symbol.upper()
        if exchange in [types.DCE, types.CZCE, types.CFFEX]:
            return symbol
        raise exception.ExchangeNotSupportedError

    @staticmethod
    def db_symbol_2_tq_symbol(symbol, exchange):
        """db symbol to tq symbol"""
        if exchange in [types.SHFE, types.INE, types.GFEX]:
            return symbol.lower()
        if exchange in [types.DCE, types.CZCE, types.CFFEX]:
            return symbol
        raise exception.ExchangeNotSupportedError

    def db_symbol_2_tq_quote(self, symbol, exchange):
        """db symbol to tq quote"""
        tq_symbol = self.db_symbol_2_tq_symbol(symbol, exchange)
        return f"{exchange}.{tq_symbol}"

    def tq_quote_2_db_variety(self, quote):
        """tq quote to variety"""
        cols = quote.split(".")
        if len(cols) != 2:
            raise ValueError("quote must be exchange.symbol like")

        exchange = cols[0]
        tq_symbol = cols[1]
        symbol = self.tq_symbol_2_db_symbol(tq_symbol, exchange)

        contract = self.dbapi.contract_get_one_by_name_exchange(symbol,
                                                                exchange)
        if not contract:
            raise exception.ContractNotFound

        return contract.variety


# pylint: disable=too-many-instance-attributes,too-many-public-methods
class TQBroker(bt.BrokerBase):
    """tq broker class"""

    def __init__(self, conf=None, notifier=None):
        super().__init__()
        self.name = "tq_broker"

        # validate the config
        self.validate_config(conf)

        # initiate source and country
        self.source = conf.source
        self.country = conf.country

        # initiate the tq client api
        self.conf = conf
        self.tq_api = self.get_tq_api()

        # initiate the db qpi
        self.dbapi = api.DBAPI(conf.db)
        self.convert = SymbolConvert(self.dbapi)

        # notifier
        self.notifier = notifier

        # initiate other attributes
        account = self._get_account_from_tq()
        self.cash = account["available"]
        self.value = account["balance"]
        self.margin = account["margin"]
        self.margin_ratio = self.margin / self.value
        self.max_margin_ratio = self.get_max_margin_ratio(conf)
        self.positions = self.get_all_positions()

        # used in backtrader
        self.startingcash = self.cash

    def get_max_margin_ratio(self, conf):
        """get max margin ratio for broker"""
        max_margin_ratio = 0.3
        if not hasattr(conf, "strategy"):
            return max_margin_ratio

        strategy_conf = conf.strategy
        if hasattr(strategy_conf, "max_margin_ratio"):
            max_margin_ratio = strategy_conf.max_margin_ratio

        return max_margin_ratio

    @staticmethod
    def validate_config(conf):
        """validate config"""

        logger.info("start validating tq config")

        tq_broker = conf.broker.tq_broker
        if not hasattr(tq_broker, "tq_username"):
            raise ValueError("tq_broker's username is not configured")
        if not hasattr(tq_broker, "tq_password"):
            raise ValueError("tq_broker's password is not configured")

        simulate = True
        if hasattr(tq_broker, "simulate"):
            simulate = tq_broker.simulate
        if not isinstance(simulate, bool):
            raise ValueError("simulate must be boolean")

        # for real trading, validate the account and password
        if not simulate:
            if not hasattr(tq_broker, "broker_id"):
                raise ValueError("tq broker's broker id not configured")

            if not hasattr(tq_broker, "account_id"):
                raise ValueError("tq broker's account id not configured")

            if not hasattr(tq_broker, "password"):
                raise ValueError("tq broker's password not configured")

        logger.info("validate tq config success")

    def get_tq_api(self):
        """initiate the api client to access the tq server."""

        logger.info("start getting tq api client")

        tq_broker = self.conf.broker.tq_broker

        # for tq auth
        tq_username = tq_broker.tq_username
        tq_password = tq_broker.tq_password
        auth = tqsdk.TqAuth(user_name=tq_username, password=tq_password)

        # for future company account
        simulate = True
        if hasattr(tq_broker, "simulate"):
            simulate = tq_broker.simulate

        # default using kq simulator account
        account = tqsdk.TqKq()
        if not simulate:
            # for real online trading account, and this account is from
            # future company.
            broker_id = tq_broker.broker_id
            account_id = tq_broker.account_id
            password = tq_broker.password
            account = tqsdk.TqAccount(broker_id=broker_id,
                                      account_id=account_id,
                                      password=password)

        tq_api = tqsdk.TqApi(account=account, auth=auth)

        logger.info("get tq api client success")

        return tq_api

    @staticmethod
    def _get_deadline(second):
        """return timeout for api.wait_update"""
        deadline = time.time() + second
        return deadline

    def _wait_update(self, second=15):
        """wait execute self.tq_api.wait_update()"""
        deadline = self._get_deadline(second)
        updated = self.tq_api.wait_update(deadline=deadline)
        return updated

    def getcash(self):
        """
        get cash

        可用资金（可用资金 = 账户权益 - 冻结保证金 - 保证金 - 冻结权利金 - 冻结手续费 - 期权市值）
        """
        return self.cash

    def get_cash(self):
        """
        get cash

        可用资金（可用资金 = 账户权益 - 冻结保证金 - 保证金 - 冻结权利金 - 冻结手续费 - 期权市值）
        """
        return self.getcash()

    def getvalue(self, datas=None):
        """
        get total value(balance)

        账户权益 （账户权益 = 动态权益 = 静态权益 + 平仓盈亏 + 持仓盈亏 - 手续费 + 权利金 + 期权市值）
        """
        return self.value

    def get_value(self, datas=None):
        """
        get total value(balance)

        账户权益 （账户权益 = 动态权益 = 静态权益 + 平仓盈亏 + 持仓盈亏 - 手续费 + 权利金 + 期权市值）
        """
        return self.getvalue(datas)

    def getposition(self, data):
        """get position by name"""
        # pylint: disable=protected-access
        position = self.positions[data._name]
        return position

    def get_all_positions(self):
        """
        get all positions, for self.tq_api.get_position(), the return Position
        """
        positions = collections.defaultdict(bt.position.Position)
        tp_positions = self._get_positions_from_tq()
        for quote, p in tp_positions.items():
            # get the variety
            variety = self.convert.tq_quote_2_db_variety(quote)
            if variety not in positions:
                positions[variety] = bt.position.Position(size=p.pos,
                                                          price=p.last_price)
            else:
                positions[variety].size += p.pos

        return positions

    def get_notification(self):
        """get notification"""
        return None

    def submit(self, order):
        raise NotImplementedError

    def cancel(self, order):
        raise NotImplementedError

    # https://doc.shinnytech.com/tqsdk/latest/usage/trade.html
    # pylint: disable=too-many-arguments,too-many-positional-arguments
    # pylint: disable=too-many-locals
    def buy(self, owner, data, size, price=None, plimit=None,
            exectype=None, valid=None, tradeid=0, oco=None,
            trailamount=None, trailpercent=None,
            **kwargs):
        """
        execute the buy by tq broker

        args:
            data: greenturtle.data.datafeed.db.ContinuousContractDB, only
                  object.p.variety matters.
            size: always positive
            kwargs: only desired maters
            others: for other parameters, they are not used yet

        buy steps:
            1. check if there are any remaining orders for the variety. if
                there are remaining orders for the variety, skip it
            2. get the currently position quote from tq server
            3. check if the current + size = desired, if it's not equal,
                than skip
            4. then perform buying
            4.1 if rolling is not needed, just buy
            4.2 rolling the contract if needed, first close the contract and
                open with the desired size
        """

        # validate parameters
        self._validate_trading_parameters(kwargs)
        variety = kwargs[types.VARIETY]
        desired_size = kwargs[types.DESIRED_SIZE]

        # check if have open order
        if self._has_open_order(variety):
            msg = f"skip buying {variety} due to remaining orders"
            self._logger_and_notifier(msg)
            return

        # get the position by variety
        position = self._get_position_from_tq_by_variety(variety)

        # check if the size are expected
        current_size = 0
        if position:
            current_size = position.pos
        if current_size + size != desired_size:
            msg = f"{variety} skip due to current {current_size}" + \
                  f" + buy {size} != desired {desired_size}"
            self._logger_and_notifier(msg)
            raise exception.BuyOrSellSizeAbnormalError

        # determine the offset and quote_name
        if desired_size > 0:
            offset = "OPEN"
            quote_name = self._get_tq_quote_from_db_by_variety(variety)
        else:
            offset = "CLOSE"
            quote_name = f"{position.exchange_id}.{position.instrument_id}"

        # get the quote and check
        quote = self._get_quote_from_tq(quote_name)
        if math.isnan(quote.ask_price1):
            msg = f"skip buy {variety} due to nan ask_price"
            self._logger_and_notifier(msg)
            return

        # do insert order
        self._insert_order_to_tq(symbol=quote_name,
                                 direction="BUY",
                                 offset=offset,
                                 limit_price=quote.ask_price1,
                                 volume=size)

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    # pylint: disable=too-many-locals
    def sell(self, owner, data, size, price=None, plimit=None,
             exectype=None, valid=None, tradeid=0, oco=None,
             trailamount=None, trailpercent=None,
             **kwargs):
        """
        execute the sell by tq broker

        args:
            owner: useless parameter
            data: <greenturtle.data.datafeed.db.ContinuousContractDB object>
            size: always positive
            kwargs: only desired maters
            others: for other parameters, they are not used yet

        sell steps:
            1. check if there are any remaining orders for the variety. if
                there are remaining orders for the variety, skip it
            2. get the currently position quote from tq server
            3. check if the current + size = desired, if it's not equal,
                than skip
            4. then perform selling
            4.1 if rolling is not needed, just sell
            4.2 rolling the contract if needed, first close the contract and
                open with the desired size
        """

        # validate parameters
        self._validate_trading_parameters(kwargs)
        variety = kwargs[types.VARIETY]
        desired_size = kwargs[types.DESIRED_SIZE]

        # check if have open order
        if self._has_open_order(variety):
            msg = f"skip selling {variety} due to remaining orders"
            self._logger_and_notifier(msg)
            return

        # get the position by variety
        position = self._get_position_from_tq_by_variety(variety)

        # check if the size are expected
        current_size = 0
        if position:
            current_size = position.pos
        if current_size != desired_size + size:
            msg = f"{variety} skip due to current {current_size}" + \
                  f" != sell {size} + desired {desired_size}"
            self._logger_and_notifier(msg)
            raise exception.BuyOrSellSizeAbnormalError

        # determine the offset and quote_name
        if desired_size < 0:
            offset = "OPEN"
            quote_name = self._get_tq_quote_from_db_by_variety(variety)
        else:
            offset = "CLOSE"
            quote_name = f"{position.exchange_id}.{position.instrument_id}"

        # get the quote and check
        quote = self._get_quote_from_tq(quote_name)
        if math.isnan(quote.bid_price1):
            msg = f"skip sell {variety} due to nan bid_price"
            self._logger_and_notifier(msg)
            return

        # do insert order
        self._insert_order_to_tq(symbol=quote_name,
                                 direction="SELL",
                                 offset=offset,
                                 limit_price=quote.bid_price1,
                                 volume=size)

    @staticmethod
    def _validate_trading_parameters(kwargs):
        """validate trading parameters"""
        if types.VARIETY not in kwargs:
            logger.error("variety not found")
            raise exception.VarietyNotFound

        if types.DESIRED_SIZE not in kwargs:
            logger.error("desired size not found")
            raise exception.DesiredSizeNotFound

    def _has_open_order(self, variety):
        """check whether there are open orders for the variety"""

        orders = self._get_orders_from_tq()
        for order in orders.values():
            # get the exchange and tq symbol from oder
            tq_symbol = order.instrument_id
            exchange = order.exchange_id

            # convert to greenturtle and try to find it from database
            symbol = self.convert.tq_symbol_2_db_symbol(tq_symbol, exchange)
            one = self.dbapi.contract_get_one_by_name_exchange(symbol,
                                                               exchange)
            if one is None:
                logger.error("contract %s not found in db", symbol)
                raise exception.ContractNotFound

            if one.variety == variety and order.status == ORDER_ALIVE:
                logger.info("find existing open order for %s", symbol)
                return True

        return False

    def _get_position_from_tq_by_variety(self, variety):
        """get positions from tq by variety"""

        positions = []
        tp_positions = self._get_positions_from_tq()

        for quote, p in tp_positions.items():
            if p.pos == 0 and p.pos_long == 0 and p.pos_short == 0:
                continue
            # get the variety
            db_variety = self.convert.tq_quote_2_db_variety(quote)
            if db_variety == variety:
                positions.append(p)

        if len(positions) > 1:
            logger.error("% has many position %s, expected 0 or 1",
                         variety, positions)
            raise exception.VarietyMultiSymbolsError

        if len(positions) == 0:
            return None

        return positions[0]

    def _get_tq_quote_from_db_by_variety(self, variety):
        """get symbol from db by variety"""
        one = self.dbapi.continuous_contract_get_latest_by_variety_source_country(  # noqa: E501
            variety, self.source, self.country)

        if one is None:
            logger.error("contract %s not found in db", variety)
            raise exception.ContractNotFound

        tq_quote = self.convert.db_symbol_2_tq_quote(one.name, one.exchange)

        return tq_quote

    def get_orders_open(self):
        """get open orders"""
        orders_open = []
        orders = self._get_orders_from_tq()
        for order in orders.values():
            if order.status == ORDER_ALIVE:
                orders_open.append(order)
        return orders_open

    def get_orders(self):
        """get all orders"""
        return self._get_orders_from_tq()

    def cancel_order(self, order_id, account=None):
        """cancel order"""
        self.tq_api.cancel_order(order_id, account=account)

    def _get_account_from_tq(self):
        """get account from tq broker"""
        logger.info("start get_account from tq broker")

        account = self.tq_api.get_account()
        updated = self._wait_update()

        logger.info("get_account _wait_update: %s", updated)

        msg = "get account from tq broker success" + \
              f"\nbalance: {account.balance:.0f}" + \
              f"\navailable: {account.available:.0f}" + \
              f"\nmargin: {account.margin:.0f}" + \
              f"\nfloat_profit: {account.float_profit:.0f}" + \
              f"\nposition_profit: {account.position_profit:.0f}"
        logger.info(msg)

        return account

    def _get_orders_from_tq(self):
        """get open orders from tq broker"""
        logger.info("start get_order from tq broker")

        orders = self.tq_api.get_order()
        updated = self._wait_update()

        logger.info("get_order _wait_update: %s", updated)

        msg = f"get {len(orders)} orders from tq broker success"
        for order in orders.values():
            if order.status == ORDER_ALIVE:
                msg += f"\n{order.exchange_id}.{order.instrument_id}" + \
                       f" {order.direction} to {order.offset}" + \
                       f" with size={order.volume_orign}" + \
                       f" at price={order.limit_price:.2f}," + \
                       f" the status is {order.status}," + \
                       f" the last message is {order.last_msg}, " + \
                       f" error {order.is_error}"
        logger.info(msg)

        return orders

    def _get_positions_from_tq(self):
        """get positions from tq broker"""
        logger.info("start get positions from tq broker")

        positions = self.tq_api.get_position()
        updated = self._wait_update()

        logger.info("get_position _wait_update: %s", updated)

        msg = f"get {len(positions)} positions from tq broker success"
        for p in positions.values():
            if p.pos_long > 0:
                value = p.open_cost_long / p.open_price_long * p.last_price
                msg += f"\n[long] {p.exchange_id}.{p.instrument_id}:" + \
                       f" size={p.pos_long}" + \
                       f" price={p.last_price:.2f}" + \
                       f" open={p.open_price_long:.2f}" + \
                       f" value={value:.0f}" + \
                       f" cost={p.open_cost_long:.0f}" + \
                       f" profit={p.float_profit_long:.0f}" + \
                       f" margin={p.margin_long:.0f}"

        for p in positions.values():
            if p.pos_short > 0:
                value = p.open_cost_short / p.open_price_short * p.last_price
                msg += f"\n[short] {p.exchange_id}.{p.instrument_id}:" + \
                       f" size={p.pos_short}" + \
                       f" price={p.last_price:.2f}" + \
                       f" open={p.open_price_short:.2f}" + \
                       f" value={value:.0f}" + \
                       f" cost={p.open_cost_short:.0f}" + \
                       f" profit={p.float_profit_short:.0f}" + \
                       f" margin={p.margin_short:.0f}"
        logger.info(msg)

        return positions

    def _get_quote_from_tq(self, quote_name):
        """get quote from tq broker"""
        logger.info("start get_quote %s from tq broker", quote_name)

        quote = self.tq_api.get_quote(quote_name)
        updated = self._wait_update()

        logger.info("get_quote %s success with _wait_update: %s",
                    quote_name, updated)

        return quote

    def _insert_order_to_tq(self,
                            symbol=None,
                            direction=None,
                            offset=None,
                            limit_price=None,
                            volume=0):
        """insert order to tq broker"""

        msg = f"start insert_order {symbol} {direction} {offset}" + \
              f" {limit_price:0.2f} {volume} to tq broker"
        self._logger_and_notifier(msg)

        if self.margin_ratio > self.max_margin_ratio:
            msg = f"skip insert_order {symbol} due to margin limitation"
            self._logger_and_notifier(msg)
            return

        self.tq_api.insert_order(symbol=symbol,
                                 direction=direction,
                                 offset=offset,
                                 limit_price=limit_price,
                                 volume=volume)
        updated = self._wait_update()
        logger.info("insert_order _wait_update: %s", updated)

        # TODO(fixeme), need to improve this step with asynchronize step.
        logger.info("insert order %s %s %s %f %d from tq broker success",
                    symbol, direction, offset, limit_price, volume)

    def account_overview(self):
        """Return account overview."""

        account = self._get_account_from_tq()
        value = account["balance"]
        cash = account["available"]
        float_profit = account["float_profit"]
        position_profit = account["position_profit"]
        margin = account["margin"]

        # account information
        msg = f"TQ broker: value {value:.0f}, cash {cash:.0f}"
        msg += f", float_profit {float_profit:.0f}"
        msg += f", position_profit {position_profit:.0f}"
        msg += f", margin {margin:.0f}."

        # position information
        rolling_list = []
        tp_positions = self._get_positions_from_tq()
        for p in tp_positions.values():
            if p.pos == 0 and p.pos_long == 0 and p.pos_short == 0:
                continue
            msg += f"\n{p.exchange_id}.{p.instrument_id}:"
            msg += f" size {p.pos}"
            msg += f" float_profit {p.float_profit:.0f}"
            msg += f" position_profit {p.position_profit:.0f}"
            msg += f" margin {p.margin:.0f};"

            actual = f"{p.exchange_id}.{p.instrument_id}"
            variety = self.convert.tq_quote_2_db_variety(actual)
            desired = self._get_tq_quote_from_db_by_variety(variety)
            if actual != desired:
                logger.info("need rolling, actual: %s, desired: %s",
                            actual, desired)
                rolling_list.append(actual)

        if len(rolling_list) > 0:
            msg += f"\nrolling list: {rolling_list}"

        # order information
        orders_open = self.get_orders_open()
        for order in orders_open:
            msg += f"\n{order.exchange_id}.{order.instrument_id}" + \
                   f" {order.direction} to {order.offset}" + \
                   f" with size={order.volume_orign}" + \
                   f" at price={order.limit_price:.2f}," + \
                   f" the status is {order.status}," + \
                   f" the last message is {order.last_msg}, " + \
                   f" error {order.is_error}"

        return msg

    def close(self):
        """close broker"""
        self.tq_api.close()
        logger.info("tq broker closed.")

    def rolling(self):
        """rolling contracts"""
        positions = self._get_positions_from_tq()
        for p in positions.values():
            # skip the position with 0 size
            if p.pos == 0 and p.pos_long == 0 and p.pos_short == 0:
                continue

            # compare the actual and desired quote name
            actual = f"{p.exchange_id}.{p.instrument_id}"
            variety = self.convert.tq_quote_2_db_variety(actual)
            desired = self._get_tq_quote_from_db_by_variety(variety)
            if actual == desired:
                logger.info("%s no need to rolling", variety)
                continue

            msg = f"{variety} need to rolling from {actual} to {desired}"
            self._logger_and_notifier(msg)

            if self._has_open_order(variety):
                msg = f"skip rolling {variety} due to open order"
                self._logger_and_notifier(msg)
                continue

            # for the long position, sell to close and then buy to open
            if p.pos_long > 0:
                self.rolling_long(p, variety, actual, desired)

            # for the short position, buy to close and then sell to open
            if p.pos_short > 0:
                self.rolling_short(p, variety, actual, desired)

    def rolling_long(self, position, variety, actual, desired):
        """rolling long contracts"""
        # prepare closing the actual contract
        quote = self._get_quote_from_tq(actual)
        if math.isnan(quote.bid_price1):
            msg = f"skip rolling {variety} due to nan bid_price"
            self._logger_and_notifier(msg)
            return

        # close the actual contract
        self._insert_order_to_tq(symbol=actual,
                                 direction="SELL",
                                 offset="CLOSE",
                                 limit_price=quote.bid_price1,
                                 volume=position.pos_long)

        # prepare opening new contract
        quote = self._get_quote_from_tq(desired)
        if math.isnan(quote.ask_price1):
            msg = f"skip rolling {variety} due to nan ask_price1"
            self._logger_and_notifier(msg)
            return

        # open the desired contract
        self._insert_order_to_tq(symbol=desired,
                                 direction="BUY",
                                 offset="OPEN",
                                 limit_price=quote.ask_price1,
                                 volume=position.pos_long)

    def rolling_short(self, position, variety, actual, desired):
        """rolling short contracts"""
        # prepare closing the actual contract
        quote = self._get_quote_from_tq(actual)
        if math.isnan(quote.ask_price1):
            msg = f"skip rolling {variety} due to nan ask_price1"
            self._logger_and_notifier(msg)
            return

        # close the actual contract by opening
        self._insert_order_to_tq(symbol=actual,
                                 direction="BUY",
                                 offset="CLOSE",
                                 limit_price=quote.ask_price1,
                                 volume=position.pos_short)

        # prepare opening new contract
        quote = self._get_quote_from_tq(desired)
        if math.isnan(quote.bid_price1):
            msg = f"skip rolling {variety} due to nan bid_price1"
            self._logger_and_notifier(msg)
            return

        # open the desired contract
        self._insert_order_to_tq(symbol=desired,
                                 direction="SELL",
                                 offset="OPEN",
                                 limit_price=quote.bid_price1,
                                 volume=position.pos_short)

    def _logger_and_notifier(self, msg):
        """logger and notifier the message"""
        logger.info(msg)
        self.notifier.send_message(msg)
