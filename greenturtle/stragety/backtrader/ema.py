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

from backtrader.indicators import MovAv
from greenturtle.stragety.backtrader import base


class EMA(base.BaseStrategy):

    """ EMA with Filter class strategy for backtrader"""

    def __init__(self, fast_period=5, slow_period=16):
        super().__init__()

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

    def should_buy(self, name):
        """determine whether a position should be bought or not."""
        fast_ema = self.fast_emas[name]
        slow_ema = self.slow_emas[name]
        return fast_ema[0] > slow_ema[0]

    def should_sell(self, name):
        """determine whether a position should be sold or not."""
        fast_ema = self.fast_emas[name]
        slow_ema = self.slow_emas[name]
        return fast_ema[0] < slow_ema[0]
