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

from greenturtle.util.logging import logging


logger = logging.get_logger()


class TQBroker(bt.BrokerBase):
    """tq broker class"""

    # TODO(fixme), symbol convertion
    # https://doc.shinnytech.com/tqsdk/latest/usage/mddatas.html
    #
    # 1. the exchange code are same between tq and db
    #       DEC  SHFE  CZCE  CFFEX  INE  GFEX
    #   db  DEC  SHFE  CZCE  CFFEX  INE  GFEX
    #   tq  DEC  SHFE  CZCE  CFFEX  INE  GFEX
    #
    # 2. the contract name are different between exchanges
    #       DEC    SHFE   CZCE   CFFEX  INE    GFEX
    #   db  lower  upper  upper  upper  upper  upper
    #   tq  lower  lower  upper  upper  lower  lower
    # for example
    #       DEC         SHFE         CZCE        CFFEX         INE         GFEX
    #   db  pg2602      SP2601       UR601       IF2504        SC2601      SI2601
    #   tq  DEC.pg2602  SHFE.sp2601  CZCE.UR601  CFFEX.IF2504  INE.sc2601  GFEX.si2601
    #

    def __init__(self, conf=None):
        super().__init__()

        self.validate_config(conf)

        self.conf = conf
        self.api = self.get_api()

        self.cash = 0.0
        self.value = 0.0
        self.positions = collections.defaultdict(bt.position.Position)

    def initiate(self):
        """initiate broker"""
        self.get_value()
        self.get_cash()
        self.get_all_positions()

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

    def get_api(self):
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

        api = tqsdk.TqApi(account=account, auth=auth)

        logger.info("get tq api client success")

        return api

    @staticmethod
    def _get_deadline(second):
        """return timeout for api.wait_update"""
        deadline = time.time() + second
        return deadline

    def _wait_update(self, second=60):
        """wait execute self.api.wait_update()"""
        deadline = self._get_deadline(second)
        self.api.wait_update(deadline=deadline)

    def getcash(self):
        """
        get cash

        可用资金（可用资金 = 账户权益 - 冻结保证金 - 保证金 - 冻结权利金 - 冻结手续费 - 期权市值）
        """
        account = self._get_account_from_tq()
        self.cash = account["available"]
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
        account = self._get_account_from_tq()
        self.value = account["balance"]
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
        get all positions, for self.api.get_position(), the return Position
        """
        tp_positions = self._get_positions_from_tq()
        for p in tp_positions:
            # TODO(fixme), data name and symbol name
            # need return a map[variety] = Position like
            self.positions[p.instrument_id] = bt.position.Position(
                size=p.pos, price=float("nan"))

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

        raise NotImplementedError

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def sell(self, owner, data, size, price=None, plimit=None,
             exectype=None, valid=None, tradeid=0, oco=None,
             trailamount=None, trailpercent=None,
             **kwargs):

        raise NotImplementedError

    def get_orders_open(self):
        """get open orders"""
        orders_open = []
        orders = self._get_orders_from_tq()
        for name, order in orders.items():
            if order.status == "ALIVE":
                orders_open.append(order)
        return orders_open

    def _get_account_from_tq(self):
        """get account from tq broker"""
        logger.info("start get account from tq broker")

        account = self.api.get_account()
        # TODO(fixme), make it as decorator
        self._wait_update()

        logger.info("get account %s from tq broker success", account)

        return account

    def _get_orders_from_tq(self):
        """get open orders from tq broker"""
        logger.info("start get order from tq broker")

        orders = self.api.get_order()
        # TODO(fixme), make it as decorator
        self._wait_update()

        logger.info("get order %s from tq broker success", orders)

        return orders

    def _get_positions_from_tq(self):
        """get positions from tq broker"""
        logger.info("start get positions from tq broker")

        positions = self.api.get_position()
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
        for name, p in tp_positions.items():
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
        self.api.close()
        logger.info("tq broker closed.")
