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
import time

import backtrader as bt
import tqsdk

from greenturtle.constants import types
from greenturtle.db import api
from greenturtle import exception
from greenturtle.util.logging import logging


logger = logging.get_logger()


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


class TQBroker(bt.BrokerBase):
    """tq broker class"""

    def __init__(self, conf=None):
        super().__init__()
        # validate the config
        self.validate_config(conf)

        # initiate the tq client api
        self.conf = conf
        self.tq_api = self.get_tq_api()

        # initiate the db qpi
        dbapi = api.DBAPI(conf.db)
        self.convert = SymbolConvert(dbapi)

        # initiate other attributes
        account = self._get_account_from_tq()
        self.cash = account["available"]
        self.value = account["balance"]
        self.positions = self.get_all_positions()

    @staticmethod
    def validate_config(conf):
        """validate config"""

        logger.info("start validating tq config")

        if not hasattr(conf, "tq_broker"):
            raise ValueError("tq_broker is not configured")

        tq_broker = conf.tq_broker
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

        tq_broker = self.conf.tq_broker

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

    def _wait_update(self, second=60):
        """wait execute self.tq_api.wait_update()"""
        deadline = self._get_deadline(second)
        self.tq_api.wait_update(deadline=deadline)

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
    def buy(self, owner, data, size, price=None, plimit=None,
            exectype=None, valid=None, tradeid=0, oco=None,
            trailamount=None, trailpercent=None,
            **kwargs):
        """
        execute the buy by tq broker

        args:
            owner: useless parameter
            data: greenturtle.data.datafeed.db.ContinuousContractDB, only
                  object.p.variety matters.
            size: always positive
            kwargs: only desired maters

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
        raise NotImplementedError

    # pylint: disable=too-many-arguments,too-many-positional-arguments
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
        raise NotImplementedError

    def get_orders_open(self):
        """get open orders"""
        orders_open = []
        orders = self._get_orders_from_tq()
        for order in orders.values():
            if order.status == "ALIVE":
                orders_open.append(order)
        return orders_open

    def _get_account_from_tq(self):
        """get account from tq broker"""
        logger.info("start get account from tq broker")

        account = self.tq_api.get_account()
        # TODO(fixme), make it as decorator
        self._wait_update()

        logger.info("get account %s from tq broker success", account)

        return account

    def _get_orders_from_tq(self):
        """get open orders from tq broker"""
        logger.info("start get order from tq broker")

        orders = self.tq_api.get_order()
        # TODO(fixme), make it as decorator
        self._wait_update()

        logger.info("get order %s from tq broker success", orders)

        return orders

    def _get_positions_from_tq(self):
        """get positions from tq broker"""
        logger.info("start get positions from tq broker")

        positions = self.tq_api.get_position()
        # TODO(fixme), make it as decorator
        self._wait_update()

        logger.info("get positions %s from tq broker success", positions)

        return positions

    def account_overview(self):
        """Return account overview."""

        account = self._get_account_from_tq()
        value = account["balance"]
        cash = account["available"]
        float_profit = account["float_profit"]
        position_profit = account["position_profit"]
        margin = account["margin"]

        # account information
        txt = f"TQ broker: value {value:.0f}, cash {cash:.0f}"
        txt += f", float_profit {float_profit:.0f}"
        txt += f", position_profit {position_profit:.0f}"
        txt += f", margin {margin:.0f}."

        # position information
        tp_positions = self._get_positions_from_tq()
        for p in tp_positions.values():
            txt += f" {p.instrument_id}: value {p.market_value:.0f}"
            txt += f" size {p.pos}"
            txt += f" float_profit {p.float_profit:.0f}"
            txt += f" position_profit {p.position_profit:.0f}"
            txt += f" margin {p.margin:.0f};"

        # order information
        orders_open = self.get_orders_open()
        for order in orders_open:
            txt += f"; order {order.order_id}, status {order.status}"

        return txt

    def close(self):
        """close broker"""
        self.tq_api.close()
        logger.info("tq broker closed.")
