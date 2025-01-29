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

""" Base strategy class for backtrader which implements some basic interface"""

import abc
import math

import backtrader as bt

import greenturtle.constants.future as future_const
from greenturtle.util.logging import logging
from greenturtle import exception


logger = logging.get_logger()


class BaseStrategy(bt.Strategy):

    """ base strategy for backtrader framework."""

    def __init__(self, allow_short=False, leverage_limit=0.95):
        super().__init__()
        self.allow_short = allow_short
        self.leverage_limit = leverage_limit
        self.order = None
        self._init_others()

    def _init_others(self):
        self.symbols_data = {}
        self.names = self.getdatanames()
        for name in self.names:
            data = self.getdatabyname(name)
            self.symbols_data[name] = data

    def _clear_order(self):
        self.order = None

    def log(self, txt, dt=None):
        """ Logging function fot this strategy."""
        dt = dt or self.datas[0].datetime.date(0)
        iso_time = dt.isoformat()
        logger.info("%s: %s", iso_time, txt)

    def start(self):
        self._clear_order()

    def next(self):
        """next function in strategy."""
        if self.order:
            return
        # 1. get the long and short hold position
        long_hold, short_hold = self.symbols_within_hold()

        # 2. compute the long and short desired position
        long_desired, short_desired = self.compute_desired_symbols()

        # 3. determine if whether need trade or not
        if long_hold != long_desired or short_hold != short_desired:
            self.log("symbols" +
                     f"\nlong hold: {sorted(list(long_hold))}" +
                     f"\nshort hold: {sorted(list(short_hold))}" +
                     f"\nlong desired: {sorted(list(long_desired))}" +
                     f"\nshort desired: {sorted(list(short_desired))}")

            # 4. get the current portfolios
            current_portfolios = self.get_current_portfolios()

            # 5. compute the desired portfolios with detailed size
            desired_portfolios = self.compute_desired_portfolios(
                long_desired,
                short_desired)

            # 6. execute the orders.
            self.execute(current_portfolios, desired_portfolios)

    def symbols_within_hold(self):
        """symbols in hold."""
        long_symbols, short_symbols = set(), set()

        positions = self.getpositions()
        for k in positions:
            # pylint: disable=protected-access
            name = k._name
            position = positions[k]
            if position.size > 0:
                long_symbols.add(name)
            elif position.size < 0:
                short_symbols.add(name)

        return long_symbols, short_symbols

    def symbols_buy_to_open(self):
        """symbols need to buy to open"""
        symbols = set()
        for name in self.names:
            if self.is_buy_to_open(name):
                symbols.add(name)

        return symbols

    def symbols_sell_to_close(self):
        """symbols need sell to close."""

        symbols = set()
        for name in self.names:
            if self.is_sell_to_close(name):
                symbols.add(name)

        return symbols

    def symbols_sell_to_open(self):
        """symbols need sell to open, only used in short size."""
        symbols = set()
        if not self.allow_short:
            return symbols

        for name in self.names:
            if self.is_sell_to_open(name):
                symbols.add(name)

        return symbols

    def symbols_buy_to_close(self):
        """symbols need buy to close, only used in short size."""
        symbols = set()
        if not self.allow_short:
            return symbols

        for name in self.names:
            if self.is_buy_to_close(name):
                symbols.add(name)

        return symbols

    @abc.abstractmethod
    def is_buy_to_open(self, name):
        """determine whether a position should buy to open or not."""
        raise NotImplementedError

    @abc.abstractmethod
    def is_sell_to_close(self, name):
        """determine whether a position should sell to close or not."""
        raise NotImplementedError

    @abc.abstractmethod
    def is_sell_to_open(self, name):
        """determine whether a position should sell to open or not."""
        raise NotImplementedError

    @abc.abstractmethod
    def is_buy_to_close(self, name):
        """determine whether a position should buy to close or not."""
        raise NotImplementedError

    def compute_desired_symbols(self):
        """compute the desired symbols"""
        buy_to_opens = self.symbols_buy_to_open()
        sell_to_closes = self.symbols_sell_to_close()
        sell_to_opens = self.symbols_sell_to_open()
        buy_to_closes = self.symbols_buy_to_close()

        # validate the operations for symbols
        self.validate(buy_to_opens, sell_to_closes, sell_to_opens,
                      buy_to_closes)

        return buy_to_opens, sell_to_opens

    def validate(self,
                 buy_to_opens,
                 sell_to_closes,
                 sell_to_opens=None,
                 buy_to_closes=None):
        """validate the symbols."""

        if sell_to_opens is None:
            sell_to_opens = set()

        if buy_to_closes is None:
            buy_to_closes = set()

        if buy_to_opens.intersection(sell_to_closes):
            raise exception.SymbolUnexpectedIntersectionError()

        if buy_to_opens.intersection(sell_to_opens):
            raise exception.SymbolUnexpectedIntersectionError()

        if sell_to_closes.intersection(buy_to_closes):
            raise exception.SymbolUnexpectedIntersectionError()

        if sell_to_opens.intersection(buy_to_closes):
            raise exception.SymbolUnexpectedIntersectionError()

    def get_current_portfolios(self):
        """get current portfolios within hold."""

        portfolios = {}
        positions = self.getpositions()

        for k in positions:
            position = positions[k]
            if position.size != 0:
                # pylint: disable=protected-access
                portfolios[k._name] = position.size

        return portfolios

    def compute_desired_portfolios(self, long_desired, short_desired):
        """compute the desired portfolio."""

        # this is the simple portfolios with average divided.
        portfolios = {}

        number = len(long_desired) + len(short_desired)
        if number == 0:
            return portfolios

        total_value = self.broker.get_value() * self.leverage_limit
        single_value = total_value / number

        for name in self.names:
            data = self.symbols_data[name]
            close = data.close[0]

            contract_unit = 1
            if hasattr(data, future_const.CONTRACT_UNIT):
                contract_unit = data.contract_unit

            contract_number = int(single_value / close / contract_unit)
            size = contract_number * contract_unit

            if name in long_desired:
                portfolios[name] = size
            if name in short_desired:
                portfolios[name] = -size

        return portfolios

    def execute(self, current_portfolios, desired_portfolios):
        """execute the orders with the following rule."""

        # 1. sell the unwanted symbols.
        for name in current_portfolios:
            if name not in desired_portfolios:
                self.order_target_size_with_log(name, 0)

        # 2. trade the symbols both in current and desired portfolios
        # 2.1 trade the symbols to get more available cash
        for name in current_portfolios:
            if name in desired_portfolios:
                current_size = current_portfolios[name]
                desired_size = desired_portfolios[name]
                if abs(current_size) > abs(desired_size):
                    self.order_target_size_with_log(name, desired_size)

        # 2.2 trade other symbols both in current and desired portfolios
        for name in current_portfolios:
            if name in desired_portfolios:
                current_size = current_portfolios[name]
                desired_size = desired_portfolios[name]
                if current_size == desired_size:
                    continue
                if abs(current_size) <= abs(desired_size):
                    self.order_target_size_with_log(name, desired_size)

        # 3. trade the new open symbols.
        for name in desired_portfolios:
            if name not in current_portfolios:
                desired_size = desired_portfolios[name]
                self.order_target_size_with_log(name, desired_size)

    def order_target_percent_with_log(self, data=None, target=0.0):
        """
        Order the target percent with loging the price.

        In most case, the strategy computing the signal with close price, and
        here is to log the close price.
        """
        if isinstance(data, str):
            data = self.getdatabyname(data)
        elif data is None:
            data = self.data

        # pylint: disable=protected-access
        name = data._name
        close = data.close[0]
        self.log(f"try to order {name} {target*100:.3f}%" +
                 f" with expected price {close:.3f}")

        self.order_target_percent(data=data, target=target)

    def order_target_size_with_log(self, data=None, size=0):
        """
        Order the target size with loging the price.

        In most case, the strategy computing the signal with close price, and
        here is to log the close price.
        """

        if isinstance(data, str):
            data = self.getdatabyname(data)
        elif data is None:
            data = self.data

        # pylint: disable=protected-access
        name = data._name
        close = data.close[0]
        value = close * size
        self.log(f"try to order {name} size: {size}" +
                 f" with price {close:.3f}, value {value:.0f}")

        self.order_target_size(data=data, target=size)

    def notify_order(self, order):
        """
        notify order response the order according to the status of the order
        and log the order.
        """

        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            # pylint: disable=protected-access
            name, price = order.data._name, order.executed.price
            size, comm = order.executed.size, order.executed.comm
            value = math.fabs(size) * price

            if order.isbuy():
                self.log(
                    f"BUY EXECUTED, name: {name}, price: {price:.3f}, " +
                    f"size: {size:.0f}, value: {value:.2f}, comm: {comm:.2f}"
                )
            elif order.issell():
                self.log(
                    f"SELL EXECUTED, name: {name}, price: {price:.3f}, " +
                    f"size: {size:.0f}, value: {value:.2f}, comm: {comm:.2f}"
                )

            total_value = self.broker.get_value()
            position = self.getpositionbyname(name)
            position_size = position.size
            position_price = position.price
            position_value = position_price * position_size
            cash = self.broker.getcash()
            self.log(
                f"total value: {total_value:.0f}, " +
                f"cash value {cash:.0f}, " +
                f"position value {position_value:.2f}, " +
                f"size: {position_size} " +
                f"price: {position_price:.3f}")

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self._clear_order()
