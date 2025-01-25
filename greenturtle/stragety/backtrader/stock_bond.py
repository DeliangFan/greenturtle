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

""" Balanced stock and bond class strategy for backtrader"""

from greenturtle.stragety.backtrader import base
from greenturtle.util.constants import constants_stock


class BalancedStockAndBondStrategy(base.BaseStrategy):

    """Balance stock and bond strategy."""

    def __init__(self):
        super().__init__()
        # the reserved_ratio is used to reduce the possibility of
        # failing orders.
        self.reserved_ratio = 0.01
        self.stock_ratio = 0.7
        self.diff_ratio = 0.05
        self.bond_ratio = 1 - self.stock_ratio - self.reserved_ratio

        # Keep a reference to the "close" for different data series.
        for data in self.datas:
            if data._name == constants_stock.STOCK:
                self.stock_close = data.close
            if data._name == constants_stock.BOND:
                self.bond_close = data.close

    def next(self):

        # Initiate the stock.
        stock_position = self.getpositionbyname(constants_stock.STOCK)
        if stock_position.size == 0:
            self.order_target_percent_with_log(
                data=constants_stock.STOCK,
                target=self.stock_ratio)

        # Initiate the stock.
        bond_position = self.getpositionbyname(constants_stock.BOND)
        if bond_position.size == 0:
            self.order_target_percent_with_log(
                data=constants_stock.BOND,
                target=self.bond_ratio)

        # Calculate the values of stock and bond.
        stock_value = stock_position.size * self.stock_close[0]
        bond_value = bond_position.size * self.bond_close[0]
        total_value = self.broker.get_value()
        stock_value_ratio = stock_value / total_value
        bond_value_ratio = bond_value / total_value

        # Re-balance between stock and bond
        if stock_value_ratio >= (self.stock_ratio + self.diff_ratio):
            self.order_target_percent_with_log(
                data=constants_stock.STOCK,
                target=self.stock_ratio)

            self.order_target_percent_with_log(
                data=constants_stock.BOND,
                target=self.bond_ratio)

        if bond_value_ratio >= (self.bond_ratio + self.diff_ratio):
            self.order_target_percent_with_log(
                data=constants_stock.BOND,
                target=self.bond_ratio)

            self.order_target_percent_with_log(
                data=constants_stock.STOCK,
                target=self.stock_ratio)

    def should_sell(self, name):
        """determine whether a position should be sold or not."""
        raise NotImplementedError

    def should_buy(self, name):
        """determine whether a position should be bought or not."""
        raise NotImplementedError
