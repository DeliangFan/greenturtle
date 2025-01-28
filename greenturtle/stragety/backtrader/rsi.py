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

""" RSI class strategy for backtrader"""

import backtrader as bt

from greenturtle.stragety.backtrader import base


class RSIStrategy(base.BaseStrategy):

    """ RSI class strategy for backtrader"""

    def __init__(self, *args, rsi_period=14, upper=70, lower=30, **kwargs):
        super().__init__(*args, **kwargs)

        self.upper = upper
        self.lower = lower
        self.rsis = {}
        for name in self.names:
            data = self.symbols_data[name]
            self.rsis[name] = bt.indicators.RSI(data, period=rsi_period)

    def is_buy_to_open(self, name):
        """determine whether a position should buy to open or not."""
        rsi = self.rsis[name]
        return rsi[0] < self.lower

    def is_sell_to_close(self, name):
        """determine whether a position should sell to close or not."""
        rsi = self.rsis[name]
        return rsi[0] > self.upper

    def is_sell_to_open(self, name):
        """determine whether a position should sell to open or not."""
        return False

    def is_buy_to_close(self, name):
        """determine whether a position should buy to close or not."""
        return False
