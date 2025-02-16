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

"""Collection of EMA strategies for backtrader"""

from backtrader.indicators import MovAv, Highest, Lowest
from greenturtle.stragety.backtrader import base


class EMA(base.BaseStrategy):

    """ EMA with Filter class strategy for backtrader"""

    def __init__(self, *args, fast_period=10, slow_period=100, **kwargs):
        super().__init__(*args, **kwargs)

        self.fast_emas = {}
        self.slow_emas = {}
        for name in self.names:
            data = self.getdatabyname(name)
            self.fast_emas[name] = MovAv.Exponential(
                data,
                period=fast_period)

            self.slow_emas[name] = MovAv.Exponential(
                data,
                period=slow_period)

    def is_buy_to_open(self, name):
        """determine whether a position should buy to open or not."""
        fast_ema = self.fast_emas[name]
        slow_ema = self.slow_emas[name]
        return fast_ema[0] > slow_ema[0]

    def is_sell_to_close(self, name):
        """determine whether a position should sell to close or not."""
        fast_ema = self.fast_emas[name]
        slow_ema = self.slow_emas[name]
        return fast_ema[0] < slow_ema[0]

    def is_sell_to_open(self, name):
        """determine whether a position should sell to open or not."""
        fast_ema = self.fast_emas[name]
        slow_ema = self.slow_emas[name]
        return fast_ema[0] < slow_ema[0]

    def is_buy_to_close(self, name):
        """determine whether a position should buy to close or not."""
        fast_ema = self.fast_emas[name]
        slow_ema = self.slow_emas[name]
        return fast_ema[0] > slow_ema[0]


class EMAEnhanced(EMA):

    """EMAEnhanced with channel class strategy for backtrader."""

    def __init__(self,
                 *args,
                 fast_period=10,
                 slow_period=100,
                 channel_period=25,
                 **kwargs):

        super().__init__(*args,
                         fast_period=fast_period,
                         slow_period=slow_period,
                         **kwargs)

        self.lowest = {}
        self.highest = {}
        for name in self.names:
            data = self.getdatabyname(name)
            self.highest[name] = Highest(data.close, period=channel_period)
            self.lowest[name] = Lowest(data.close, period=channel_period)

    def is_buy_to_open(self, name):
        """determine whether a position should buy to open or not."""
        data = self.getdatabyname(name)
        data_close = data.close[0]
        fast_ema = self.fast_emas[name]
        slow_ema = self.slow_emas[name]
        highest = self.highest[name]
        return fast_ema[0] > slow_ema[0] and data_close >= highest[0]

    def is_sell_to_close(self, name):
        """determine whether a position should sell to close or not."""
        # condition a, compare the fast and slow line
        fast_ema = self.fast_emas[name]
        slow_ema = self.slow_emas[name]

        # condition b, check the stop condition by atr
        data = self.getdatabyname(name)
        data_close = data.close[0]
        highest = self.highest[name]
        atr = self.atrs[name]
        stop = highest[0] >= data_close + 3 * atr[0]

        return fast_ema[0] < slow_ema[0] or stop

    def is_sell_to_open(self, name):
        """determine whether a position should sell to close or not."""
        data = self.getdatabyname(name)
        data_close = data.close[0]
        fast_ema = self.fast_emas[name]
        slow_ema = self.slow_emas[name]
        lowest = self.lowest[name]
        return fast_ema[0] < slow_ema[0] and data_close <= lowest[0]

    def is_buy_to_close(self, name):
        """determine whether a position should buy to close or not."""
        # condition a, compare the fast and slow line
        fast_ema = self.fast_emas[name]
        slow_ema = self.slow_emas[name]

        # condition b, check the stop condition by atr
        data = self.getdatabyname(name)
        data_close = data.close[0]
        lowest = self.lowest[name]
        atr = self.atrs[name]
        stop = data_close >= lowest[0] + 3 * atr[0]

        return fast_ema[0] > slow_ema[0] or stop
