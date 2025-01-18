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

    def __init__(self, period=18, upper=1.1, lower=0.7):
        super().__init__()
        self.period = period
        # according to the experiment in btc, the performance depends a lot
        # on the upper and lower parameters.
        # pylint: disable=unexpected-keyword-arg
        self.rsrs = rsrs.RSRS(period=period)
        self.upper = upper
        self.lower = lower

    def next(self):
        if self.order or self.rsrs[0] <= -1:
            return

        if self.position:
            if self.rsrs[0] <= self.lower:
                self.order_target_percent_with_log(
                    data=self.data,
                    target=0)
        # not in the market
        else:
            if self.rsrs[0] >= self.upper:
                self.order_target_percent_with_log(
                    data=self.data,
                    target=self.target)
