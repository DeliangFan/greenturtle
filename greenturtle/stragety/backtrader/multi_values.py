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

"""Multi-Value class strategy for backtrader"""

import backtrader as bt

from greenturtle.stragety.backtrader import base
from greenturtle.util.logging import logging


logger = logging.get_logger()


class MultiValueStrategy(base.BaseStrategy):

    """Multi value class strategy for backtrader"""

    def __init__(self,
                 period_me1=12,
                 period_me2=26,
                 period_signal=9,
                 atr_period=14):

        super().__init__()
        self.symbols_data = {}
        self.macds = {}
        self.atrs = {}
        self.names = self.getdatanames()
        for name in self.names:
            data = self.getdatabyname(name)
            self.symbols_data[name] = data
            # pylint: disable=too-many-function-args,unexpected-keyword-arg
            self.macds[name] = bt.indicators.MACD(
                                        data,
                                        period_me1=period_me1,
                                        period_me2=period_me2,
                                        period_signal=period_signal)

            # Set the stop price
            self.atrs[name] = bt.indicators.ATR(data, period=atr_period)

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
                f"current symbols: {symbols}," +
                f"desired symbols: {desired_symbols}" +
                f"symbols to be bought: {bought_symbols}," +
                f"symbols to be sold: {sold_sysmbols},")

            desired_portfolios = self.compute_desired_portfolios(
                desired_symbols)
            self.execute(sold_sysmbols, desired_portfolios)

    def should_sell(self, name):
        """determine whether a position should be sold or not."""
        macd = self.macds[name]
        # TODO(refine the code)
        diff = macd.macd[0] - macd.signal[0]
        return diff < -0.05 * macd.signal[0]

    def should_buy(self, name):
        """determine whether a position should be bought or not."""
        macd = self.macds[name]
        # TODO(refine the code)
        diff = macd.macd[0] - macd.signal[0]
        return diff > -0.01 * macd.signal[0]

    def get_symbols_within_positions(self):
        """symbols in the positions."""
        symbols = set()

        positions = self.getpositions()
        for k in positions:
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
            portfolio = min(0.95 / len(symbols), 0.25)
            portfolios[name] = portfolio

        return portfolios

    def execute(self, sold_sysmbols, desired_portfolios):
        """execute the orders."""

        total_value = self.broker.get_value() * 1.0

        # sell the unwanted symbols first.
        for name in sold_sysmbols:
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
