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

""" MACD class strategy for backtrader"""

import backtrader as bt
from greenturtle.stragety.backtrader import base


class MACDStrategy(base.BaseStrategy):

    """ MACD class strategy for backtrader"""

    # Standard MACD Parameters
    def __init__(self, period_me1=12, period_me2=26, period_signal=9):
        super().__init__()

        # TODO(wsfdl), figure out the theory about the parameters in python3
        # Keep a reference to the "close" line in the data[0] dataseries
        self.target_ratio = 1.0

        # pylint: disable=too-many-function-args,unexpected-keyword-arg
        self.macd = bt.indicators.MACD(self.data,
                                       period_me1=period_me1,
                                       period_me2=period_me2,
                                       period_signal=period_signal)

    def next(self):
        if self.order:
            return

        # valina macd strategy
        #
        # if self.position and self.mcross[0] < 0:
        #     self.order_target_percent(target=0)
        # elif not self.position and self.mcross[0] > 0:
        #     self.order_target_percent(target=1.0)
        #
        # The following optimized strategy works better in both btc and eth
        # in the market
        diff = self.macd.macd[0] - self.macd.signal[0]
        if self.position:
            if diff < -0.05 * self.macd.signal[0]:
                self.order_target_percent(target=0)
        # not in the market
        else:
            if diff > -0.01 * self.macd.signal[0]:
                self.order_target_percent(target=1.0)
