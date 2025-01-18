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

    params = (
        # Standard MIM Parameters
        ('period', 14),
    )

    def __init__(self, rsi_period=14, upper=70, lower=30):
        super().__init__()
        # Keep a reference to the "close" line in the data[0] dataseries
        self.upper = upper
        self.lower = lower
        self.rsi = bt.indicators.RSI(period=rsi_period)

    def next(self):
        if self.order:
            return

        if self.position:
            if self.rsi[0] > self.upper:
                self.order_target_percent_with_log(
                    data=self.data,
                    target=0)
        # not in the market
        else:
            if self.rsi[0] < self.lower:
                self.order_target_percent_with_log(
                    data=self.data,
                    target=self.target)
