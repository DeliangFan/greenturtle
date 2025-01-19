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
        self.short_period = short_period
        self.long_period = long_period
        self.data_close = self.data.close
        self.long_highest = Highest(self.data.high, period=self.long_period)
        self.long_lowest = Lowest(self.data.low, period=self.long_period)
        self.short_highest = Highest(self.data.high, period=self.short_period)
        self.short_lowest = Lowest(self.data.low, period=self.short_period)

    def next(self):
        if self.order:
            return

        if self.position:
            if self.data_close[0] <= self.short_lowest[-1]:
                self.order_target_percent_with_log(
                    data=self.data,
                    target=0)
        # not in the market
        else:
            if self.data_close[0] >= self.long_highest[-1]:
                self.order_target_percent_with_log(
                    data=self.data,
                    target=self.target)
