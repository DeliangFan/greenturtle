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

""" MIM class strategy for backtrader"""

from backtrader.indicators import MovAv
from greenturtle.stragety.backtrader import base


class MIMStrategy(base.BaseStrategy):

    """ MIM class strategy for backtrader"""

    params = (
        # Standard MIM Parameters
        ('period', 100),
    )

    def __init__(self):
        super().__init__()
        # Keep a reference to the "close" line in the data[0] dataseries
        self.target_ratio = 1.0
        self.movav = MovAv.Exponential(self.data, period=self.p.period)

    def next(self):
        if self.order:
            return

        if self.position:
            if self.data[0] < self.movav[0]:
                self.order_target_percent_with_log(
                    data=self.data,
                    target=0)
        # not in the market
        else:
            if self.data[0] > self.movav[0]:
                self.order_target_percent_with_log(
                    data=self.data,
                    target=self.target)
