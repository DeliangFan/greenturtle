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

    def __init__(self, rsi_period=14, upper=70, lower=30):
        super().__init__()

        self.upper = upper
        self.lower = lower
        self.rsis = {}
        for name in self.names:
            data = self.symbols_data[name]
            self.rsis[name] = bt.indicators.RSI(data, period=rsi_period)

    def should_buy(self, name):
        """determine whether a position should be bought or not."""
        rsi = self.rsis[name]
        return rsi[0] < self.lower

    def should_sell(self, name):
        """determine whether a position should be sold or not."""
        rsi = self.rsis[name]
        return rsi[0] > self.upper
