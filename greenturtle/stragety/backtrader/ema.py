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
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.data_close = self.data.close
        self.fast_ema = MovAv.Exponential(
            self.data_close,
            period=self.fast_period)
        self.slow_ema = MovAv.Exponential(
            self.data_close,
            period=self.slow_period)

    def next(self):
        if self.order:
            return

        if self.position:
            if self.fast_ema[0] < self.slow_ema[0]:
                # sell
                self.order_target_percent_with_log(
                    data=self.data,
                    target=0)
        # not in the market
        else:
            if self.fast_ema[0] > self.slow_ema[0]:
                # buy
                self.order_target_percent_with_log(
                    data=self.data,
                    target=self.target)
