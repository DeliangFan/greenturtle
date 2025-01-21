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


class RefinedMACDStrategy(base.BaseStrategy):

    """ MACD class strategy for backtrader"""

    # Standard MACD Parameters
    def __init__(self, period_me1=12, period_me2=26, period_signal=9):
        super().__init__()

        # pylint: disable=too-many-function-args,unexpected-keyword-arg
        self.macd = bt.indicators.MACD(self.data0,
                                       period_me1=period_me1,
                                       period_me2=period_me2,
                                       period_signal=period_signal)

    def next(self):
        if self.order:
            return

        # valina macd strategy
        #
        # if self.position and self.mcross[0] < 0:
        #     self.order_target_percent_with_log(data=self.data, target=0)
        # elif not self.position and self.mcross[0] > 0:
        #     self.order_target_percent_with_log(data=self.data, target=1.0)
        #
        # The following optimized strategy works better in both btc and eth
        # in the market
        diff = self.macd.macd[0] - self.macd.signal[0]
        if self.position:
            if diff < -0.05 * self.macd.signal[0]:
                # sell
                self.order_target_percent_with_log(
                    data=self.data0,
                    target=0)
        # not in the market
        else:
            if diff > -0.01 * self.macd.signal[0]:
                # buy
                self.order_target_percent_with_log(
                    data=self.data0,
                    target=self.target)


# MACDWithATRStrategy is copied from backtrader/samples/macd-settings.py
class MACDWithATRStrategy(base.BaseStrategy):
    """
    This strategy is loosely based on some of the examples from the Van
    K. Tharp book: *Trade Your Way To Financial Freedom*. The logic:

      - Enter the market if:
        - The MACD.macd line crosses the MACD.signal line to the upside
        - The Simple Moving Average has a negative direction in the last x
          periods (actual value below value x periods ago)

     - Set a stop price x times the ATR value away from the close

     - If in the market:

       - Check if the current close has gone below the stop price. If yes,
         exit.
       - If not, update the stop price if the new stop price would be higher
         than the current
    """

    params = (
        # Standard MACD Parameters
        ('macd1', 12),
        ('macd2', 26),
        ('macdsig', 9),
        ('atrperiod', 14),  # ATR Period (standard)
        ('atrdist', 3.0),   # ATR distance for stop price
        ('smaperiod', 30),  # SMA Period (pretty standard)
        ('dirperiod', 10),  # Lookback period to consider SMA trend direction
    )

    # pylint: disable=too-many-positional-arguments,too-many-arguments
    def __init__(self,
                 period_me1=12,
                 period_me2=26,
                 period_signal=9,
                 atr_period=14,
                 atr_dist=3.0,
                 sma_period=30,
                 dir_period=10):
        super().__init__()
        self.atr_dist = atr_dist
        self.pstop = 0

        # pylint: disable=unexpected-keyword-arg,too-many-function-args
        self.macd = bt.indicators.MACD(self.data,
                                       period_me1=period_me1,
                                       period_me2=period_me2,
                                       period_signal=period_signal)

        # Cross of macd.macd and macd.signal
        # pylint: disable=unexpected-keyword-arg,too-many-function-args
        self.mcross = bt.indicators.CrossOver(self.macd.macd, self.macd.signal)

        # To set the stop price
        self.atr = bt.indicators.ATR(self.data, period=atr_period)

        # Control market trend
        self.sma = bt.indicators.SMA(self.data, period=sma_period)
        self.smadir = self.sma - self.sma(-dir_period)

    def next(self):
        if self.order:
            return  # pending order execution

        if not self.position:  # not in the market
            if self.mcross[0] > 0.0 > self.smadir:
                # buy
                self.order_target_percent_with_log(
                    data=self.data,
                    target=self.target)

                pdist = self.atr[0] * self.atr_dist
                self.pstop = self.data.close[0] - pdist

        else:  # in the market
            pclose = self.data.close[0]

            if pclose < self.pstop:
                # sell
                self.order_target_percent_with_log(
                    data=self.data,
                    target=0)  # stop met - get out
            else:
                pdist = self.atr[0] * self.atr_dist
                # Update only if greater than
                self.pstop = max(self.pstop, pclose - pdist)
