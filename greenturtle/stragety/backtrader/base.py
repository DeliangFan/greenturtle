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

import math

import backtrader as bt

from greenturtle.util.logging import logging


logger = logging.get_logger()
MAX_PORTFOLIO_PER_SYMBOL = 0.95
TOTAL_PORTFOLIO = 0.95


class BaseStrategy(bt.Strategy):

    """ base strategy for backtrader framework."""

    def __init__(self):
        super().__init__()
        self.order = None
        self.target = TOTAL_PORTFOLIO
        self.symbols_data = {}
        self.names = self.getdatanames()
        for name in self.names:
            data = self.getdatabyname(name)
            self.symbols_data[name] = data

    def log(self, txt, dt=None):
        """ Logging function fot this strategy."""
        dt = dt or self.datas[0].datetime.date(0)
        iso_time = dt.isoformat()
        logger.info("%s: %s", iso_time, txt)

    def start(self):
        self.order = None

    def next(self):
        """
        1. get the hold position
        2. compute the position to sell
        3. compute the position to buy
        4. compute the desired position list
        5. compute the desired portfolio
        6. execute
        """
        if self.order:
            return

        symbols = self.get_symbols_within_positions()

        bought_symbols = self.symbols_to_be_bought()
        desired_symbols = symbols.union(bought_symbols)

        sold_sysmbols = self.symbols_to_be_sold()
        desired_symbols = desired_symbols.difference(sold_sysmbols)

        if symbols != desired_symbols:
            self.log(
                f"symbols\ncurrent: {sorted(list(symbols))}" +
                f"\ndesired: {sorted(list(desired_symbols))}" +
                f"\nbuy: {sorted(list(bought_symbols))}," +
                f"\nsell: {sorted(list(sold_sysmbols))},")

            desired_portfolios = self.compute_desired_portfolios(
                desired_symbols)
            self.execute(sold_sysmbols, desired_portfolios)

    def get_symbols_within_positions(self):
        """symbols in the positions."""
        symbols = set()

        positions = self.getpositions()
        for k in positions:
            position = positions[k]
            if position.size != 0:
                # pylint: disable=protected-access
                symbols.add(k._name)

        return symbols

    def symbols_to_be_sold(self):
        """symbols in the position which should be sold."""
        symbols = set()

        positions = self.get_symbols_within_positions()
        for name in positions:
            if self.should_sell(name):
                symbols.add(name)

        return symbols

    def symbols_to_be_bought(self):
        """symbols not in the position which should be bought."""

        symbols = set()

        positions = self.get_symbols_within_positions()
        for name in self.names:
            if name in positions:
                continue
            if self.should_buy(name):
                symbols.add(name)

        return symbols

    def compute_desired_portfolios(self, symbols):
        """
        compute the desired portfolio
        1. no symbols will more than 25%.
        """

        portfolios = {}
        for name in symbols:
            portfolio = min(
                TOTAL_PORTFOLIO / len(symbols),
                MAX_PORTFOLIO_PER_SYMBOL)
            portfolios[name] = portfolio

        return portfolios

    def execute(self, sold_sysmbols, desired_portfolios):
        """execute the orders."""

        total_value = self.broker.get_value() * 1.0

        # sell the unwanted symbols first.
        for name in sold_sysmbols:
            position = self.getpositionbyname(name)
            if position.size != 0:
                self.order_target_percent_with_log(name, 0)

        # trade the symbols with position more than desired
        positions = self.getpositions()
        for k in positions:
            # pylint: disable=protected-access
            name = k._name
            if name in desired_portfolios:
                position = positions[k]
                position_value = position.size * position.price
                current_portfolio = position_value / total_value
                desired_portfolio = desired_portfolios[name]
                if current_portfolio > desired_portfolio:
                    self.order_target_percent_with_log(name, desired_portfolio)
                    desired_portfolios.pop(name)

        # trade the remaining symbols
        for name in desired_portfolios:
            portfolio = desired_portfolios[name]
            self.order_target_percent_with_log(name, portfolio)

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
            self.log(
                f"total value: {total_value:.2f}, " +
                f"position value {position_value:.2f}, " +
                f"size: {position_size} " +
                f"price: {position_price:.3f}")

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def should_sell(self, name):
        """determine whether a position should be sold or not."""
        raise NotImplementedError

    def should_buy(self, name):
        """determine whether a position should be bought or not."""
        raise NotImplementedError
