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

from greenturtle.constants.future import types
from greenturtle.constants.future import varieties
import greenturtle.data.backtrader.future as future_data
from greenturtle.simulator.backtrader import future_simulator
from greenturtle.stragety.backtrader import buyhold
from greenturtle.stragety.backtrader import channel
from greenturtle.stragety.backtrader import ema
from greenturtle.stragety.backtrader import macd
from greenturtle.stragety.backtrader import mim
from greenturtle.stragety.backtrader import rsi


# pylint: disable=R0801
class TestBasicFutureBacktrader(unittest.TestCase):
    """e2e test for future within backtrader."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.future_data = {}
        self.fromdate = datetime(2001, 1, 1)
        self.todate = datetime(2024, 12, 31)

        for group in varieties.US_VARIETIES.values():
            for name, future in group.items():

                # skip if not downloadable from yahoo.
                # pylint: disable=invalid-name
                if types.YAHOO_CODE not in future:
                    continue

                yahoo_code = future[types.YAHOO_CODE]

                # get feed data from yahoo finance
                data = future_data.get_feed_from_yahoo_finance(
                    yahoo_code,
                    name=name,
                    fromdate=self.fromdate,
                    todate=self.todate)

                self.future_data[name] = data

    def setUp(self):
        self.s = future_simulator.FutureSimulator()

    @unittest.skip('Fix me!')
    def test_future_with_buy_and_hold(self):
        """test buy and hold future."""

        name = "GC"
        data = self.future_data[name]
        self.s.add_data(data, name)
        self.s.add_strategy(buyhold.BuyHoldStrategy, leverage_limit=0.2)
        self.s.set_default_commission_by_name(name)
        self.s.do_simulate()

        return_summary = self.s.summary.return_summary
        self.assertEqual(1903, int(return_summary.total_return))
        self.assertEqual(13.4, round(return_summary.annual_return, 1))

        sharpe_ratio_summary = self.s.summary.sharpe_ratio_summary
        self.assertEqual(0.76, round(sharpe_ratio_summary.sharpe_ratio, 2))

        max_draw_down_summary = self.s.summary.max_draw_down_summary
        self.assertEqual(48.1, round(max_draw_down_summary.max_draw_down, 1))

        leverage_ratio_summary = self.s.summary.leverage_ratio_summary
        self.assertEqual(0.11,
                         round(leverage_ratio_summary.leverage_ratio, 2))

    @unittest.skip('Fix me!')
    def test_future_with_ema(self):
        """test trade future with ema strategy."""

        name = "GC"
        data = self.future_data[name]
        self.s.add_data(data, name)
        self.s.add_strategy(ema.EMA, leverage_limit=0.2)
        self.s.set_default_commission_by_name(name)
        self.s.do_simulate()

        # test the return summary
        return_summary = self.s.summary.return_summary
        self.assertEqual(523, int(return_summary.total_return))
        self.assertEqual(8.0, round(return_summary.annual_return, 1))

        # test the sharpe ratio summary
        sharpe_ratio_summary = self.s.summary.sharpe_ratio_summary
        self.assertEqual(0.40, round(sharpe_ratio_summary.sharpe_ratio, 2))

        # test the max draw down summary
        max_draw_down_summary = self.s.summary.max_draw_down_summary
        self.assertEqual(63.6, round(max_draw_down_summary.max_draw_down, 1))

        # test the leverage ratio summary
        leverage_ratio_summary = self.s.summary.leverage_ratio_summary
        self.assertEqual(
            0.12,
            round(leverage_ratio_summary.leverage_ratio, 2))

        # test the trade summary
        trade_summary = self.s.summary.trade_summary
        self.assertEqual(2674, int(trade_summary.net / 1000))
        self.assertEqual(2699, int(trade_summary.gross / 1000))
        self.assertEqual(8706, int(trade_summary.won / 1000))
        self.assertEqual(-6031, int(trade_summary.lost / 1000))
        self.assertEqual(61, trade_summary.trader_number)
        self.assertEqual(23, trade_summary.win_trader_number)

        # test the position profit and lost summary
        positions_pnl_summary = self.s.summary.positions_pnl_summary
        positions_pnl = positions_pnl_summary.positions_pnl
        self.assertIn(name, positions_pnl)

        position_pnl = positions_pnl[name]
        self.assertEqual(2674, int(position_pnl["net"] / 1000))
        self.assertEqual(2699, int(position_pnl["gross"] / 1000))
        self.assertEqual(-6031, int(position_pnl["lost"] / 1000))
        self.assertEqual(60, position_pnl["trade_number"])

    @unittest.skip('Fix me!')
    def test_future_with_mim(self):
        """test trade future with mim strategy."""

        name = "GC"
        data = self.future_data[name]
        self.s.add_data(data, name)
        self.s.add_strategy(mim.MIMStrategy, leverage_limit=0.2)
        self.s.set_default_commission_by_name(name)
        self.s.do_simulate()

        # test the return summary
        return_summary = self.s.summary.return_summary
        self.assertEqual(569, int(return_summary.total_return))
        self.assertEqual(8.3, round(return_summary.annual_return, 1))

        # test the sharpe ratio summary
        sharpe_ratio_summary = self.s.summary.sharpe_ratio_summary
        self.assertEqual(0.43, round(sharpe_ratio_summary.sharpe_ratio, 2))

        # test the max draw down summary
        max_draw_down_summary = self.s.summary.max_draw_down_summary
        self.assertEqual(56.9, round(max_draw_down_summary.max_draw_down, 1))

        # test the leverage ratio summary
        leverage_ratio_summary = self.s.summary.leverage_ratio_summary
        self.assertEqual(
            0.12,
            round(leverage_ratio_summary.leverage_ratio, 2))

        # test the trade summary
        trade_summary = self.s.summary.trade_summary
        self.assertEqual(3052, int(trade_summary.net / 1000))
        self.assertEqual(3125, int(trade_summary.gross / 1000))
        self.assertEqual(10579, int(trade_summary.won / 1000))
        self.assertEqual(-7526, int(trade_summary.lost / 1000))
        self.assertEqual(188, trade_summary.trader_number)
        self.assertEqual(51, trade_summary.win_trader_number)

        # test the position profit and lost summary
        positions_pnl_summary = self.s.summary.positions_pnl_summary
        positions_pnl = positions_pnl_summary.positions_pnl
        self.assertIn(name, positions_pnl)

        position_pnl = positions_pnl[name]
        self.assertEqual(3052, int(position_pnl["net"] / 1000))
        self.assertEqual(3125, int(position_pnl["gross"] / 1000))
        self.assertEqual(-7526, int(position_pnl["lost"] / 1000))
        self.assertEqual(187, position_pnl["trade_number"])

    @unittest.skip('Fix me!')
    def test_future_with_channel(self):
        """test trade future with channel strategy."""

        name = "GC"
        data = self.future_data[name]
        self.s.add_data(data, name)
        self.s.add_strategy(channel.DonchianChannel, leverage_limit=0.2)
        self.s.set_default_commission_by_name(name)
        self.s.do_simulate()

        # test the return summary
        return_summary = self.s.summary.return_summary
        self.assertEqual(62, int(return_summary.total_return))
        self.assertEqual(2.0, round(return_summary.annual_return, 1))

        # test the sharpe ratio summary
        sharpe_ratio_summary = self.s.summary.sharpe_ratio_summary
        self.assertEqual(0.16, round(sharpe_ratio_summary.sharpe_ratio, 2))

        # test the max draw down summary
        max_draw_down_summary = self.s.summary.max_draw_down_summary
        self.assertEqual(26.5, round(max_draw_down_summary.max_draw_down, 1))

        # test the leverage ratio summary
        leverage_ratio_summary = self.s.summary.leverage_ratio_summary
        self.assertEqual(
            0.01,
            round(leverage_ratio_summary.leverage_ratio, 2))

        # test the trade summary
        trade_summary = self.s.summary.trade_summary
        self.assertEqual(623, int(trade_summary.net / 1000))
        self.assertEqual(681, int(trade_summary.gross / 1000))
        self.assertEqual(2952, int(trade_summary.won / 1000))
        self.assertEqual(-2329, int(trade_summary.lost / 1000))
        self.assertEqual(242, trade_summary.trader_number)
        self.assertEqual(121, trade_summary.win_trader_number)

        # test the position profit and lost summary
        positions_pnl_summary = self.s.summary.positions_pnl_summary
        positions_pnl = positions_pnl_summary.positions_pnl
        self.assertIn(name, positions_pnl)

        position_pnl = positions_pnl[name]
        self.assertEqual(623, int(position_pnl["net"] / 1000))
        self.assertEqual(681, int(position_pnl["gross"] / 1000))
        self.assertEqual(-2329, int(position_pnl["lost"] / 1000))
        self.assertEqual(242, position_pnl["trade_number"])

    @unittest.skip('Fix me!')
    def test_future_with_macd(self):
        """test trade future with macd strategy."""

        name = "GC"
        data = self.future_data[name]
        self.s.add_data(data, name)
        self.s.add_strategy(macd.MACDWithATRStrategy, leverage_limit=0.2)
        self.s.set_default_commission_by_name(name)
        self.s.do_simulate()

        # test the return summary
        return_summary = self.s.summary.return_summary
        self.assertEqual(-2, int(return_summary.total_return))
        self.assertEqual(-0.1, round(return_summary.annual_return, 1))

        # test the sharpe ratio summary
        sharpe_ratio_summary = self.s.summary.sharpe_ratio_summary
        self.assertEqual(-0.23, round(sharpe_ratio_summary.sharpe_ratio, 2))

        # test the max draw down summary
        max_draw_down_summary = self.s.summary.max_draw_down_summary
        self.assertEqual(22.0, round(max_draw_down_summary.max_draw_down, 1))

        # test the leverage ratio summary
        leverage_ratio_summary = self.s.summary.leverage_ratio_summary
        self.assertEqual(
            0.00,
            round(leverage_ratio_summary.leverage_ratio, 2))

        # test the trade summary
        trade_summary = self.s.summary.trade_summary
        self.assertEqual(-27, int(trade_summary.net / 1000))
        self.assertEqual(-3, int(trade_summary.gross / 1000))
        self.assertEqual(872, int(trade_summary.won / 1000))
        self.assertEqual(-899, int(trade_summary.lost / 1000))
        self.assertEqual(134, trade_summary.trader_number)
        self.assertEqual(71, trade_summary.win_trader_number)

        # test the position profit and lost summary
        positions_pnl_summary = self.s.summary.positions_pnl_summary
        positions_pnl = positions_pnl_summary.positions_pnl
        self.assertIn(name, positions_pnl)

        position_pnl = positions_pnl[name]
        self.assertEqual(-27, int(position_pnl["net"] / 1000))
        self.assertEqual(-3, int(position_pnl["gross"] / 1000))
        self.assertEqual(-899, int(position_pnl["lost"] / 1000))
        self.assertEqual(134, position_pnl["trade_number"])

    @unittest.skip('Fix me!')
    def test_future_with_rsi(self):
        """test trade future with rsi strategy."""

        name = "GC"
        data = self.future_data[name]
        self.s.add_data(data, name)
        self.s.add_strategy(rsi.RSIStrategy, leverage_limit=0.2)
        self.s.set_default_commission_by_name(name)
        self.s.do_simulate()

        # test the return summary
        return_summary = self.s.summary.return_summary
        self.assertEqual(7, int(return_summary.total_return))
        self.assertEqual(0.3, round(return_summary.annual_return, 1))

        # test the sharpe ratio summary
        sharpe_ratio_summary = self.s.summary.sharpe_ratio_summary
        self.assertEqual(-0.18, round(sharpe_ratio_summary.sharpe_ratio, 2))

        # test the max draw down summary
        max_draw_down_summary = self.s.summary.max_draw_down_summary
        self.assertEqual(20.1, round(max_draw_down_summary.max_draw_down, 1))

        # test the leverage ratio summary
        leverage_ratio_summary = self.s.summary.leverage_ratio_summary
        self.assertEqual(
            0.01,
            round(leverage_ratio_summary.leverage_ratio, 2))

        # test the trade summary
        trade_summary = self.s.summary.trade_summary
        self.assertEqual(74, int(trade_summary.net / 1000))
        self.assertEqual(82, int(trade_summary.gross / 1000))
        self.assertEqual(653, int(trade_summary.won / 1000))
        self.assertEqual(-579, int(trade_summary.lost / 1000))
        self.assertEqual(52, trade_summary.trader_number)
        self.assertEqual(33, trade_summary.win_trader_number)

        # test the position profit and lost summary
        positions_pnl_summary = self.s.summary.positions_pnl_summary
        positions_pnl = positions_pnl_summary.positions_pnl
        self.assertIn(name, positions_pnl)

        position_pnl = positions_pnl[name]
        self.assertEqual(74, int(position_pnl["net"] / 1000))
        self.assertEqual(82, int(position_pnl["gross"] / 1000))
        self.assertEqual(-579, int(position_pnl["lost"] / 1000))
        self.assertEqual(52, position_pnl["trade_number"])
