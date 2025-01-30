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

"""some basic e2e test for stock"""

from datetime import datetime
import unittest

import greenturtle.constants.stock as stock_const
import greenturtle.data.backtrader.stock as stock_data
from greenturtle.simulator.backtrader import simulator
from greenturtle.stragety.backtrader import buyhold
from greenturtle.stragety.backtrader import channel
from greenturtle.stragety.backtrader import ema
from greenturtle.stragety.backtrader import macd
from greenturtle.stragety.backtrader import mim
from greenturtle.stragety.backtrader import rsi
from greenturtle.stragety.backtrader import stock_bond


class TestBasicStockBacktrader(unittest.TestCase):
    """e2e test for stock within backtrader."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fromdate = datetime(2000, 1, 1)
        self.todate = datetime(2024, 1, 1)

        self.name = stock_const.QQQ
        self.data = stock_data.get_feed_from_yahoo_finance(
            self.name,
            fromdate=self.fromdate,
            todate=self.todate)

    def setUp(self):
        self.s = simulator.Simulator(commission=0, slippage=0)

    def test_stock_with_buy_and_hold(self):
        """test buy and hold stock."""

        self.s.add_data(self.data, self.name)
        self.s.add_strategy(buyhold.BuyHoldStrategy)
        self.s.do_simulate()

        return_summary = self.s.summary.return_summary
        self.assertEqual(392, int(return_summary.total_return))
        self.assertEqual(6.9, round(return_summary.annual_return, 1))

        sharpe_ratio_summary = self.s.summary.sharpe_ratio_summary
        self.assertEqual(0.36, round(sharpe_ratio_summary.sharpe_ratio, 2))

        max_draw_down_summary = self.s.summary.max_draw_down_summary
        self.assertEqual(75.6, round(max_draw_down_summary.max_draw_down, 1))

        leverage_ratio_summary = self.s.summary.leverage_ratio_summary
        self.assertEqual(
            0.86,
            round(leverage_ratio_summary.leverage_ratio, 2))

    def test_stock_with_ema(self):
        """test trade stock with ema strategy."""

        self.s.add_data(self.data, self.name)
        self.s.add_strategy(ema.EMA)
        self.s.do_simulate()

        # test the return summary
        return_summary = self.s.summary.return_summary
        self.assertEqual(377, int(return_summary.total_return))
        self.assertEqual(6.7, round(return_summary.annual_return, 1))

        # test the sharpe ratio summary
        sharpe_ratio_summary = self.s.summary.sharpe_ratio_summary
        self.assertEqual(0.4, round(sharpe_ratio_summary.sharpe_ratio, 2))

        # test the max draw down summary
        max_draw_down_summary = self.s.summary.max_draw_down_summary
        self.assertEqual(34.5, round(max_draw_down_summary.max_draw_down, 1))

        # test the leverage ratio summary
        leverage_ratio_summary = self.s.summary.leverage_ratio_summary
        self.assertEqual(
            0.66,
            round(leverage_ratio_summary.leverage_ratio, 2))

        # test the trade summary
        trade_summary = self.s.summary.trade_summary
        self.assertEqual(3354, int(trade_summary.net / 1000))
        self.assertEqual(3354, int(trade_summary.gross / 1000))
        self.assertEqual(4773, int(trade_summary.won / 1000))
        self.assertEqual(-1418, int(trade_summary.lost / 1000))
        self.assertEqual(46, trade_summary.trader_number)
        self.assertEqual(19, trade_summary.win_trader_number)

        # test the position profit and lost summary
        positions_pnl_summary = self.s.summary.positions_pnl_summary
        positions_pnl = positions_pnl_summary.positions_pnl
        self.assertIn(self.name, positions_pnl)

        position_pnl = positions_pnl[self.name]
        self.assertEqual(3354, int(position_pnl["net"] / 1000))
        self.assertEqual(3354, int(position_pnl["gross"] / 1000))
        self.assertEqual(-1418, int(position_pnl["lost"] / 1000))
        self.assertEqual(45, position_pnl["trade_number"])

    def test_stock_with_mim(self):
        """test trade stock with mim strategy."""

        self.s.add_data(self.data, self.name)
        self.s.add_strategy(mim.MIMStrategy)
        self.s.do_simulate()

        # test the return summary
        return_summary = self.s.summary.return_summary
        self.assertEqual(501, int(return_summary.total_return))
        self.assertEqual(7.8, round(return_summary.annual_return, 1))

        # test the sharpe ratio summary
        sharpe_ratio_summary = self.s.summary.sharpe_ratio_summary
        self.assertEqual(0.45, round(sharpe_ratio_summary.sharpe_ratio, 2))

        # test the max draw down summary
        max_draw_down_summary = self.s.summary.max_draw_down_summary
        self.assertEqual(34.2, round(max_draw_down_summary.max_draw_down, 1))

        # test the leverage ratio summary
        leverage_ratio_summary = self.s.summary.leverage_ratio_summary
        self.assertEqual(
            0.65,
            round(leverage_ratio_summary.leverage_ratio, 2))

        # test the trade summary
        trade_summary = self.s.summary.trade_summary
        self.assertEqual(4413, int(trade_summary.net / 1000))
        self.assertEqual(4413, int(trade_summary.gross / 1000))
        self.assertEqual(7163, int(trade_summary.won / 1000))
        self.assertEqual(-2749, int(trade_summary.lost / 1000))
        self.assertEqual(148, trade_summary.trader_number)
        self.assertEqual(65, trade_summary.win_trader_number)

        # test the position profit and lost summary
        positions_pnl_summary = self.s.summary.positions_pnl_summary
        positions_pnl = positions_pnl_summary.positions_pnl
        self.assertIn(self.name, positions_pnl)

        position_pnl = positions_pnl[self.name]
        self.assertEqual(4413, int(position_pnl["net"] / 1000))
        self.assertEqual(4413, int(position_pnl["gross"] / 1000))
        self.assertEqual(-2749, int(position_pnl["lost"] / 1000))
        self.assertEqual(147, position_pnl["trade_number"])

    def test_stock_with_channel(self):
        """test trade stock with channel strategy."""

        self.s.add_data(self.data, self.name)
        self.s.add_strategy(channel.DonchianChannel)
        self.s.do_simulate()

        # test the return summary
        return_summary = self.s.summary.return_summary
        self.assertEqual(-7, int(return_summary.total_return))
        self.assertEqual(-0.3, round(return_summary.annual_return, 1))

        # test the sharpe ratio summary
        sharpe_ratio_summary = self.s.summary.sharpe_ratio_summary
        self.assertEqual(-0.26, round(sharpe_ratio_summary.sharpe_ratio, 2))

        # test the max draw down summary
        max_draw_down_summary = self.s.summary.max_draw_down_summary
        self.assertEqual(34.1, round(max_draw_down_summary.max_draw_down, 1))

        # test the leverage ratio summary
        leverage_ratio_summary = self.s.summary.leverage_ratio_summary
        self.assertEqual(
            0.15,
            round(leverage_ratio_summary.leverage_ratio, 2))

        # test the trade summary
        trade_summary = self.s.summary.trade_summary
        self.assertEqual(-74, int(trade_summary.net / 1000))
        self.assertEqual(-74, int(trade_summary.gross / 1000))
        self.assertEqual(1632, int(trade_summary.won / 1000))
        self.assertEqual(-1707, int(trade_summary.lost / 1000))
        self.assertEqual(411, trade_summary.trader_number)
        self.assertEqual(218, trade_summary.win_trader_number)

        # test the position profit and lost summary
        positions_pnl_summary = self.s.summary.positions_pnl_summary
        positions_pnl = positions_pnl_summary.positions_pnl
        self.assertIn(self.name, positions_pnl)

        position_pnl = positions_pnl[self.name]
        self.assertEqual(-74, int(position_pnl["net"] / 1000))
        self.assertEqual(-74, int(position_pnl["gross"] / 1000))
        self.assertEqual(-1707, int(position_pnl["lost"] / 1000))
        self.assertEqual(411, position_pnl["trade_number"])

    def test_stock_with_macd(self):
        """test trade stock with macd strategy."""

        self.s.add_data(self.data, self.name)
        self.s.add_strategy(macd.MACDWithATRStrategy)
        self.s.do_simulate()

        # test the return summary
        return_summary = self.s.summary.return_summary
        self.assertEqual(-2, int(return_summary.total_return))
        self.assertEqual(-0.1, round(return_summary.annual_return, 1))

        # test the sharpe ratio summary
        sharpe_ratio_summary = self.s.summary.sharpe_ratio_summary
        self.assertEqual(-0.35, round(sharpe_ratio_summary.sharpe_ratio, 2))

        # test the max draw down summary
        max_draw_down_summary = self.s.summary.max_draw_down_summary
        self.assertEqual(20.1, round(max_draw_down_summary.max_draw_down, 1))

        # test the leverage ratio summary
        leverage_ratio_summary = self.s.summary.leverage_ratio_summary
        self.assertEqual(
            0.02,
            round(leverage_ratio_summary.leverage_ratio, 2))

        # test the trade summary
        trade_summary = self.s.summary.trade_summary
        self.assertEqual(-28, int(trade_summary.net / 1000))
        self.assertEqual(-28, int(trade_summary.gross / 1000))
        self.assertEqual(726, int(trade_summary.won / 1000))
        self.assertEqual(-754, int(trade_summary.lost / 1000))
        self.assertEqual(116, trade_summary.trader_number)
        self.assertEqual(67, trade_summary.win_trader_number)

        # test the position profit and lost summary
        positions_pnl_summary = self.s.summary.positions_pnl_summary
        positions_pnl = positions_pnl_summary.positions_pnl
        self.assertIn(self.name, positions_pnl)

        position_pnl = positions_pnl[self.name]
        self.assertEqual(-28, int(position_pnl["net"] / 1000))
        self.assertEqual(-28, int(position_pnl["gross"] / 1000))
        self.assertEqual(-754, int(position_pnl["lost"] / 1000))
        self.assertEqual(116, position_pnl["trade_number"])

    def test_stock_with_rsi(self):
        """test trade stock with rsi strategy."""

        self.s.add_data(self.data, self.name)
        self.s.add_strategy(rsi.RSIStrategy)
        self.s.do_simulate()

        # test the return summary
        return_summary = self.s.summary.return_summary
        self.assertEqual(46, int(return_summary.total_return))
        self.assertEqual(1.6, round(return_summary.annual_return, 1))

        # test the sharpe ratio summary
        sharpe_ratio_summary = self.s.summary.sharpe_ratio_summary
        self.assertEqual(0.16, round(sharpe_ratio_summary.sharpe_ratio, 2))

        # test the max draw down summary
        max_draw_down_summary = self.s.summary.max_draw_down_summary
        self.assertEqual(17.8, round(max_draw_down_summary.max_draw_down, 1))

        # test the leverage ratio summary
        leverage_ratio_summary = self.s.summary.leverage_ratio_summary
        self.assertEqual(
            0.01,
            round(leverage_ratio_summary.leverage_ratio, 2))

        # test the trade summary
        trade_summary = self.s.summary.trade_summary
        self.assertEqual(463, int(trade_summary.net / 1000))
        self.assertEqual(463, int(trade_summary.gross / 1000))
        self.assertEqual(921, int(trade_summary.won / 1000))
        self.assertEqual(-458, int(trade_summary.lost / 1000))
        self.assertEqual(45, trade_summary.trader_number)
        self.assertEqual(29, trade_summary.win_trader_number)

        # test the position profit and lost summary
        positions_pnl_summary = self.s.summary.positions_pnl_summary
        positions_pnl = positions_pnl_summary.positions_pnl
        self.assertIn(self.name, positions_pnl)

        position_pnl = positions_pnl[self.name]
        self.assertEqual(463, int(position_pnl["net"] / 1000))
        self.assertEqual(463, int(position_pnl["gross"] / 1000))
        self.assertEqual(-458, int(position_pnl["lost"] / 1000))
        self.assertEqual(45, position_pnl["trade_number"])

    def test_stock_bond_balanced(self):
        """test trade stock and bond balanced strategy."""

        # add stock data
        data = stock_data.get_feed_from_yahoo_finance(
            stock_const.VFIAX,
            fromdate=self.fromdate,
            todate=self.todate)
        self.s.add_data(data, stock_const.STOCK)

        # add tlt bond
        data = stock_data.get_feed_from_yahoo_finance(
            stock_const.TLT,
            fromdate=self.fromdate,
            todate=self.todate)
        self.s.add_data(data, stock_const.BOND)

        self.s.add_strategy(stock_bond.BalancedStockAndBondStrategy)
        self.s.do_simulate()

        # test the return summary
        return_summary = self.s.summary.return_summary
        self.assertEqual(526, int(return_summary.total_return))
        self.assertEqual(8.3, round(return_summary.annual_return, 1))

        # test the sharpe ratio summary
        sharpe_ratio_summary = self.s.summary.sharpe_ratio_summary
        self.assertEqual(0.66, round(sharpe_ratio_summary.sharpe_ratio, 2))

        # test the max draw down summary
        max_draw_down_summary = self.s.summary.max_draw_down_summary
        self.assertEqual(36.8, round(max_draw_down_summary.max_draw_down, 1))

        # test the leverage ratio summary
        leverage_ratio_summary = self.s.summary.leverage_ratio_summary
        self.assertEqual(
            0.92,
            round(leverage_ratio_summary.leverage_ratio, 2))
