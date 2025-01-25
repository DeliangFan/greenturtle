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

""" Channel class strategy for backtrader"""

from backtrader.indicators import Highest, Lowest
from greenturtle.stragety.backtrader import base


class DonchianChannel(base.BaseStrategy):

    """
    DonchianChannel class strategy for backtrader.

    Actually, the channel is not good comparing to the EMVA line.
    """

    def __init__(self, short_period=25, long_period=50):
        super().__init__()

        self.long_highests = {}
        self.long_lowests = {}
        self.short_highests = {}
        self.short_lowests = {}
        for name in self.names:
            data = self.symbols_data[name]
            self.long_highests[name] = Highest(data.high, period=long_period)
            self.long_lowests[name] = Lowest(data.low, period=long_period)
            self.short_highests[name] = Highest(data.high, period=short_period)
            self.short_lowests[name] = Lowest(data.low, period=short_period)

    def should_buy(self, name):
        """determine whether a position should be bought or not."""
        data = self.symbols_data[name]
        long_highest = self.long_highests[name]
        return data.close[0] >= long_highest[-1]

    def should_sell(self, name):
        """determine whether a position should be sold or not."""
        data = self.symbols_data[name]
        short_lowest = self.short_lowests[name]
        return data.close[0] <= short_lowest[-1]
