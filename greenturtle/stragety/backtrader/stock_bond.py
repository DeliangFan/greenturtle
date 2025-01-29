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

import greenturtle.constants.stock as stock_const
from greenturtle.stragety.backtrader import base


class BalancedStockAndBondStrategy(base.BaseStrategy):

    """Balance stock and bond strategy."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # the reserved_ratio is used to reduce the possibility of
        # failing orders.
        self.reserved_ratio = 0.01
        self.stock_ratio = 0.7
        self.diff_ratio = 0.05
        self.bond_ratio = 1 - self.stock_ratio - self.reserved_ratio

        # Keep a reference to the "close" for different data series.
        for data in self.datas:
            if data._name == stock_const.STOCK:
                self.stock_close = data.close
            if data._name == stock_const.BOND:
                self.bond_close = data.close

    def next(self):

        # Initiate the stock.
        stock_position = self.getpositionbyname(stock_const.STOCK)
        if stock_position.size == 0:
            self.order_target_percent_with_log(
                data=stock_const.STOCK,
                target=self.stock_ratio)

        # Initiate the stock.
        bond_position = self.getpositionbyname(stock_const.BOND)
        if bond_position.size == 0:
            self.order_target_percent_with_log(
                data=stock_const.BOND,
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
                data=stock_const.STOCK,
                target=self.stock_ratio)

            self.order_target_percent_with_log(
                data=stock_const.BOND,
                target=self.bond_ratio)

        if bond_value_ratio >= (self.bond_ratio + self.diff_ratio):
            self.order_target_percent_with_log(
                data=stock_const.BOND,
                target=self.bond_ratio)

            self.order_target_percent_with_log(
                data=stock_const.STOCK,
                target=self.stock_ratio)

    def is_buy_to_open(self, name):
        """determine whether a position should buy to open or not."""
        return False

    def is_sell_to_close(self, name):
        """determine whether a position should sell to close or not."""
        return False

    def is_sell_to_open(self, name):
        """determine whether a position should sell to open or not."""
        return False

    def is_buy_to_close(self, name):
        """determine whether a position should buy to close or not."""
        return False
