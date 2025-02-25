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

"""some basic e2e test for future"""

from datetime import datetime
import unittest

from greenturtle.constants.future import varieties
import greenturtle.data.datafeed.future as future_data
from greenturtle.simulator import future_simulator
from greenturtle.stragety import buyhold
from greenturtle.stragety import channel
from greenturtle.stragety import ema
from greenturtle.stragety import macd
from greenturtle.stragety import mim
from greenturtle.stragety import rsi


# pylint: disable=R0801
class TestBasicFutureBacktrader(unittest.TestCase):
    """e2e test for future within backtrader."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.future_data = {}
        self.fromdate = datetime(2022, 1, 1)
        self.todate = datetime(2024, 12, 31)
        self.name = "GC"
        self.yahoo_code = "GC=F"

    def setUp(self):
        self.s = future_simulator.FutureSimulator(
            varieties=varieties.US_VARIETIES)

    def test_future_with_buy_and_hold(self):
        """test buy and hold future."""

        data = future_data.get_feed_from_yahoo_finance(
                    self.yahoo_code,
                    name=self.name,
                    fromdate=self.fromdate,
                    todate=self.todate)
        self.s.add_data(data, self.name)
        self.s.add_strategy(buyhold.BuyHoldStrategy, leverage_limit=0.2)
        self.s.set_default_commission_by_name(self.name)
        self.s.do_simulate()

        return_summary = self.s.summary.return_summary
        self.assertEqual(7, int(return_summary.total_return))
        self.assertEqual(2.4, round(return_summary.annual_return, 1))

        sharpe_ratio_summary = self.s.summary.sharpe_ratio_summary
        self.assertEqual(0.58, round(sharpe_ratio_summary.sharpe_ratio, 2))

        max_draw_down_summary = self.s.summary.max_draw_down_summary
        self.assertEqual(2.5, round(max_draw_down_summary.max_draw_down, 1))

        leverage_ratio_summary = self.s.summary.leverage_ratio_summary
        self.assertEqual(0.01,
                         round(leverage_ratio_summary.leverage_ratio, 2))

    def test_future_with_ema(self):
        """test trade future with ema strategy."""

        data = future_data.get_feed_from_yahoo_finance(
                    self.yahoo_code,
                    name=self.name,
                    fromdate=self.fromdate,
                    todate=self.todate)
        self.s.add_data(data, self.name)
        self.s.add_strategy(ema.EMA, leverage_limit=0.2, atr_period=99)
        self.s.set_default_commission_by_name(self.name)
        self.s.do_simulate()

        # test the return summary
        return_summary = self.s.summary.return_summary
        self.assertEqual(6, int(return_summary.total_return))
        self.assertEqual(2.1, round(return_summary.annual_return, 1))

        # test the sharpe ratio summary
        sharpe_ratio_summary = self.s.summary.sharpe_ratio_summary
        self.assertEqual(0.42, round(sharpe_ratio_summary.sharpe_ratio, 2))

        # test the max draw down summary
        max_draw_down_summary = self.s.summary.max_draw_down_summary
        self.assertEqual(2.3, round(max_draw_down_summary.max_draw_down, 1))

        # test the leverage ratio summary
        leverage_ratio_summary = self.s.summary.leverage_ratio_summary
        self.assertEqual(
            0.01,
            round(leverage_ratio_summary.leverage_ratio, 2))

        # test the trade summary
        trade_summary = self.s.summary.trade_summary
        self.assertEqual(-4, int(trade_summary.net / 1000))

    def test_future_with_mim(self):
        """test trade future with mim strategy."""

        data = future_data.get_feed_from_yahoo_finance(
                    self.yahoo_code,
                    name=self.name,
                    fromdate=self.fromdate,
                    todate=self.todate)
        self.s.add_data(data, self.name)
        self.s.add_strategy(mim.MIMStrategy, leverage_limit=0.2)
        self.s.set_default_commission_by_name(self.name)
        self.s.do_simulate()

        # test the return summary
        return_summary = self.s.summary.return_summary
        self.assertEqual(6, int(return_summary.total_return))
        self.assertEqual(2.2, round(return_summary.annual_return, 1))

        # test the sharpe ratio summary
        sharpe_ratio_summary = self.s.summary.sharpe_ratio_summary
        self.assertEqual(0.49, round(sharpe_ratio_summary.sharpe_ratio, 2))

        # test the max draw down summary
        max_draw_down_summary = self.s.summary.max_draw_down_summary
        self.assertEqual(2.3, round(max_draw_down_summary.max_draw_down, 1))

        # test the leverage ratio summary
        leverage_ratio_summary = self.s.summary.leverage_ratio_summary
        self.assertEqual(
            0.01,
            round(leverage_ratio_summary.leverage_ratio, 2))

    def test_future_with_channel(self):
        """test trade future with channel strategy."""

        data = future_data.get_feed_from_yahoo_finance(
                    self.yahoo_code,
                    name=self.name,
                    fromdate=self.fromdate,
                    todate=self.todate)
        self.s.add_data(data, self.name)
        self.s.add_strategy(channel.DonchianChannel, leverage_limit=0.2)
        self.s.set_default_commission_by_name(self.name)
        self.s.do_simulate()

        # test the return summary
        return_summary = self.s.summary.return_summary
        self.assertEqual(4, int(return_summary.total_return))
        self.assertEqual(1.4, round(return_summary.annual_return, 1))

    def test_future_with_macd(self):
        """test trade future with macd strategy."""

        data = future_data.get_feed_from_yahoo_finance(
                    self.yahoo_code,
                    name=self.name,
                    fromdate=self.fromdate,
                    todate=self.todate)
        self.s.add_data(data, self.name)
        self.s.add_strategy(macd.MACDWithATRStrategy, leverage_limit=0.2)
        self.s.set_default_commission_by_name(self.name)
        self.s.do_simulate()

        # test the return summary
        return_summary = self.s.summary.return_summary
        self.assertEqual(5, int(return_summary.total_return))
        self.assertEqual(1.9, round(return_summary.annual_return, 1))

    def test_future_with_rsi(self):
        """test trade future with rsi strategy."""

        data = future_data.get_feed_from_yahoo_finance(
            self.yahoo_code,
            name=self.name,
            fromdate=self.fromdate,
            todate=self.todate)
        self.s.add_data(data, self.name)
        self.s.add_strategy(rsi.RSIStrategy, leverage_limit=0.2)
        self.s.set_default_commission_by_name(self.name)
        self.s.do_simulate()

        # test the return summary
        return_summary = self.s.summary.return_summary
        self.assertEqual(0, int(return_summary.total_return))
        self.assertEqual(0.3, round(return_summary.annual_return, 1))
