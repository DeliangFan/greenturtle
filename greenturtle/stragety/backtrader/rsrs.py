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

""" RSRS class strategy for backtrader"""


from greenturtle.indicators.backtrader import rsrs
from greenturtle.stragety.backtrader import base


class RSRSStrategy(base.BaseStrategy):

    """
    RSRS class strategy for backtrader.

    RSRS is short for resistence support relative strength.

    光大证券 <基于阻力支撑相对强度的市场择时>
    """

    def __init__(self, *args, period=18, upper=1.1, lower=0.7, **kwargs):
        super().__init__(*args, **kwargs)

        self.upper = upper
        self.lower = lower
        self.rsrses = {}
        # according to the experiment in btc, the performance depends a lot
        # on the upper and lower parameters.
        for name in self.names:
            data = self.symbols_data[name]
            # pylint: disable=unexpected-keyword-arg,too-many-function-args
            self.rsrses[name] = rsrs.RSRS(data, period=period)

    def is_buy_to_open(self, name):
        """determine whether a position should buy to open or not."""
        r = self.rsrses[name]
        return r[0] >= self.upper

    def is_sell_to_close(self, name):
        """determine whether a position should sell to close or not."""
        r = self.rsrses[name]
        return r[0] <= self.lower

    def is_sell_to_open(self, name):
        """determine whether a position should sell to open or not."""
        return False

    def is_buy_to_close(self, name):
        """determine whether a position should buy to close or not."""
        return False
