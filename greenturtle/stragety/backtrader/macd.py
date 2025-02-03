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
                 *args,
                 period_me1=12,
                 period_me2=26,
                 period_signal=9,
                 atr_period=14,
                 atr_dist=3.0,
                 sma_period=30,
                 dir_period=10,
                 **kwargs):

        super().__init__(*args, **kwargs)

        self.atr_dist = atr_dist
        self.pstops = {}
        self.macds = {}
        self.mcrosses = {}
        self.atrs = {}
        self.smas = {}
        self.smadirs = {}

        for name in self.names:
            self.pstops[name] = 0
            data = self.getdatabyname(name)

            # pylint: disable=unexpected-keyword-arg,too-many-function-args
            macd = bt.indicators.MACD(
                data,
                period_me1=period_me1,
                period_me2=period_me2,
                period_signal=period_signal)

            self.macds[name] = macd

            # Cross of macd.macd and macd.signal
            # pylint: disable=unexpected-keyword-arg,too-many-function-args
            self.mcrosses[name] = bt.indicators.CrossOver(
                macd.macd,
                macd.signal)

            # To set the stop price
            self.atrs[name] = bt.indicators.ATR(data, period=atr_period)

            # Control market trend
            sma = bt.indicators.SMA(data, period=sma_period)
            self.smas[name] = sma
            self.smadirs[name] = sma - sma(-dir_period)

    def is_buy_to_open(self, name):
        """determine whether a position should buy to open or not."""

        mcross = self.mcrosses[name]
        smadir = self.smadirs[name]
        data = self.symbols_data[name]
        atr = self.atrs[name]

        if mcross[0] > 0.0 > smadir:
            pdist = atr[0] * self.atr_dist
            self.pstops[name] = data.close[0] - pdist
            return True
        return False

    def is_sell_to_close(self, name):
        """determine whether a position should sell to close or not."""

        data = self.symbols_data[name]
        atr = self.atrs[name]
        pstop = self.pstops[name]
        pclose = data.close[0]

        if pstop > pclose:
            return True

        pdist = atr[0] * self.atr_dist
        self.pstops[name] = max(pstop, pclose - pdist)

        return False

    def is_sell_to_open(self, name):
        """determine whether a position should sell to open or not."""
        return False

    def is_buy_to_close(self, name):
        """determine whether a position should buy to close or not."""
        return False
