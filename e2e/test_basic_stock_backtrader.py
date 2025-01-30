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
        self.assertEqual(int(return_summary.total_return), 392)
        self.assertEqual(round(return_summary.annual_return, 1), 6.9)

        sharpe_ratio_summary = self.s.summary.sharpe_ratio_summary
        self.assertEqual(round(sharpe_ratio_summary.sharpe_ratio, 2), 0.36)

        max_draw_down_summary = self.s.summary.max_draw_down_summary
        self.assertEqual(round(max_draw_down_summary.max_draw_down, 1), 75.6)

        leverage_ratio_summary = self.s.summary.leverage_ratio_summary
        self.assertEqual(
            round(leverage_ratio_summary.leverage_ratio, 2),
            0.86)

    def test_stock_with_ema(self):
        """test trade stock with ema strategy."""

        self.s.add_data(self.data, self.name)
        self.s.add_strategy(ema.EMA)
        self.s.do_simulate()

        # test the return summary
        return_summary = self.s.summary.return_summary
        self.assertEqual(int(return_summary.total_return), 377)
        self.assertEqual(round(return_summary.annual_return, 1), 6.7)

        # test the sharpe ratio summary
        sharpe_ratio_summary = self.s.summary.sharpe_ratio_summary
        self.assertEqual(round(sharpe_ratio_summary.sharpe_ratio, 2), 0.4)

        # test the max draw down summary
        max_draw_down_summary = self.s.summary.max_draw_down_summary
        self.assertEqual(round(max_draw_down_summary.max_draw_down, 1), 34.5)

        # test the leverage ratio summary
        leverage_ratio_summary = self.s.summary.leverage_ratio_summary
        self.assertEqual(
            round(leverage_ratio_summary.leverage_ratio, 2),
            0.66)

        # test the trade summary
        trade_summary = self.s.summary.trade_summary
        self.assertEqual(int(trade_summary.net / 1000), 3354)
        self.assertEqual(int(trade_summary.gross / 1000), 3354)
        self.assertEqual(int(trade_summary.won / 1000), 4773)
        self.assertEqual(int(trade_summary.lost / 1000), -1418)
        self.assertEqual(trade_summary.trader_number, 46)
        self.assertEqual(trade_summary.win_trader_number, 19)

        # test the position profit and lost summary
        positions_pnl_summary = self.s.summary.positions_pnl_summary
        positions_pnl = positions_pnl_summary.positions_pnl
        self.assertIn(self.name, positions_pnl)

        position_pnl = positions_pnl[self.name]
        self.assertEqual(int(position_pnl["net"] / 1000), 3354)
        self.assertEqual(int(position_pnl["gross"] / 1000), 3354)
        self.assertEqual(int(position_pnl["lost"] / 1000), -1418)
        self.assertEqual(position_pnl["trade_number"], 45)

    def test_stock_with_mim(self):
        """test trade stock with mim strategy."""

        self.s.add_data(self.data, self.name)
        self.s.add_strategy(mim.MIMStrategy)
        self.s.do_simulate()

        # test the return summary
        return_summary = self.s.summary.return_summary
        self.assertEqual(int(return_summary.total_return), 501)
        self.assertEqual(round(return_summary.annual_return, 1), 7.8)

        # test the sharpe ratio summary
        sharpe_ratio_summary = self.s.summary.sharpe_ratio_summary
        self.assertEqual(round(sharpe_ratio_summary.sharpe_ratio, 2), 0.45)

        # test the max draw down summary
        max_draw_down_summary = self.s.summary.max_draw_down_summary
        self.assertEqual(round(max_draw_down_summary.max_draw_down, 1), 34.2)

        # test the leverage ratio summary
        leverage_ratio_summary = self.s.summary.leverage_ratio_summary
        self.assertEqual(
            round(leverage_ratio_summary.leverage_ratio, 2),
            0.65)

        # test the trade summary
        trade_summary = self.s.summary.trade_summary
        self.assertEqual(int(trade_summary.net / 1000), 4413)
        self.assertEqual(int(trade_summary.gross / 1000), 4413)
        self.assertEqual(int(trade_summary.won / 1000), 7163)
        self.assertEqual(int(trade_summary.lost / 1000), -2749)
        self.assertEqual(trade_summary.trader_number, 148)
        self.assertEqual(trade_summary.win_trader_number, 65)

        # test the position profit and lost summary
        positions_pnl_summary = self.s.summary.positions_pnl_summary
        positions_pnl = positions_pnl_summary.positions_pnl
        self.assertIn(self.name, positions_pnl)

        position_pnl = positions_pnl[self.name]
        self.assertEqual(int(position_pnl["net"] / 1000), 4413)
        self.assertEqual(int(position_pnl["gross"] / 1000), 4413)
        self.assertEqual(int(position_pnl["lost"] / 1000), -2749)
        self.assertEqual(position_pnl["trade_number"], 147)

    def test_stock_with_channel(self):
        """test trade stock with channel strategy."""

        self.s.add_data(self.data, self.name)
        self.s.add_strategy(channel.DonchianChannel)
        self.s.do_simulate()

        # test the return summary
        return_summary = self.s.summary.return_summary
        self.assertEqual(int(return_summary.total_return), -7)
        self.assertEqual(round(return_summary.annual_return, 1), -0.3)

        # test the sharpe ratio summary
        sharpe_ratio_summary = self.s.summary.sharpe_ratio_summary
        self.assertEqual(round(sharpe_ratio_summary.sharpe_ratio, 2), -0.26)

        # test the max draw down summary
        max_draw_down_summary = self.s.summary.max_draw_down_summary
        self.assertEqual(round(max_draw_down_summary.max_draw_down, 1), 34.1)

        # test the leverage ratio summary
        leverage_ratio_summary = self.s.summary.leverage_ratio_summary
        self.assertEqual(
            round(leverage_ratio_summary.leverage_ratio, 2),
            0.15)

        # test the trade summary
        trade_summary = self.s.summary.trade_summary
        self.assertEqual(int(trade_summary.net / 1000), -74)
        self.assertEqual(int(trade_summary.gross / 1000), -74)
        self.assertEqual(int(trade_summary.won / 1000), 1632)
        self.assertEqual(int(trade_summary.lost / 1000), -1707)
        self.assertEqual(trade_summary.trader_number, 411)
        self.assertEqual(trade_summary.win_trader_number, 218)

        # test the position profit and lost summary
        positions_pnl_summary = self.s.summary.positions_pnl_summary
        positions_pnl = positions_pnl_summary.positions_pnl
        self.assertIn(self.name, positions_pnl)

        position_pnl = positions_pnl[self.name]
        self.assertEqual(int(position_pnl["net"] / 1000), -74)
        self.assertEqual(int(position_pnl["gross"] / 1000), -74)
        self.assertEqual(int(position_pnl["lost"] / 1000), -1707)
        self.assertEqual(position_pnl["trade_number"], 411)

    def test_stock_with_macd(self):
        """test trade stock with macd strategy."""

        self.s.add_data(self.data, self.name)
        self.s.add_strategy(macd.MACDWithATRStrategy)
        self.s.do_simulate()

        # test the return summary
        return_summary = self.s.summary.return_summary
        self.assertEqual(int(return_summary.total_return), -2)
        self.assertEqual(round(return_summary.annual_return, 1), -0.1)

        # test the sharpe ratio summary
        sharpe_ratio_summary = self.s.summary.sharpe_ratio_summary
        self.assertEqual(round(sharpe_ratio_summary.sharpe_ratio, 2), -0.35)

        # test the max draw down summary
        max_draw_down_summary = self.s.summary.max_draw_down_summary
        self.assertEqual(round(max_draw_down_summary.max_draw_down, 1), 20.1)

        # test the leverage ratio summary
        leverage_ratio_summary = self.s.summary.leverage_ratio_summary
        self.assertEqual(
            round(leverage_ratio_summary.leverage_ratio, 2),
            0.02)

        # test the trade summary
        trade_summary = self.s.summary.trade_summary
        self.assertEqual(int(trade_summary.net / 1000), -28)
        self.assertEqual(int(trade_summary.gross / 1000), -28)
        self.assertEqual(int(trade_summary.won / 1000), 726)
        self.assertEqual(int(trade_summary.lost / 1000), -754)
        self.assertEqual(trade_summary.trader_number, 116)
        self.assertEqual(trade_summary.win_trader_number, 67)

        # test the position profit and lost summary
        positions_pnl_summary = self.s.summary.positions_pnl_summary
        positions_pnl = positions_pnl_summary.positions_pnl
        self.assertIn(self.name, positions_pnl)

        position_pnl = positions_pnl[self.name]
        self.assertEqual(int(position_pnl["net"] / 1000), -28)
        self.assertEqual(int(position_pnl["gross"] / 1000), -28)
        self.assertEqual(int(position_pnl["lost"] / 1000), -754)
        self.assertEqual(position_pnl["trade_number"], 116)

    def test_stock_with_rsi(self):
        """test trade stock with rsi strategy."""

        self.s.add_data(self.data, self.name)
        self.s.add_strategy(rsi.RSIStrategy)
        self.s.do_simulate()

        # test the return summary
        return_summary = self.s.summary.return_summary
        self.assertEqual(int(return_summary.total_return), 46)
        self.assertEqual(round(return_summary.annual_return, 1), 1.6)

        # test the sharpe ratio summary
        sharpe_ratio_summary = self.s.summary.sharpe_ratio_summary
        self.assertEqual(round(sharpe_ratio_summary.sharpe_ratio, 2), 0.16)

        # test the max draw down summary
        max_draw_down_summary = self.s.summary.max_draw_down_summary
        self.assertEqual(round(max_draw_down_summary.max_draw_down, 1), 17.8)

        # test the leverage ratio summary
        leverage_ratio_summary = self.s.summary.leverage_ratio_summary
        self.assertEqual(
            round(leverage_ratio_summary.leverage_ratio, 2),
            0.01)

        # test the trade summary
        trade_summary = self.s.summary.trade_summary
        self.assertEqual(int(trade_summary.net / 1000), 463)
        self.assertEqual(int(trade_summary.gross / 1000), 463)
        self.assertEqual(int(trade_summary.won / 1000), 921)
        self.assertEqual(int(trade_summary.lost / 1000), -458)
        self.assertEqual(trade_summary.trader_number, 45)
        self.assertEqual(trade_summary.win_trader_number, 29)

        # test the position profit and lost summary
        positions_pnl_summary = self.s.summary.positions_pnl_summary
        positions_pnl = positions_pnl_summary.positions_pnl
        self.assertIn(self.name, positions_pnl)

        position_pnl = positions_pnl[self.name]
        self.assertEqual(int(position_pnl["net"] / 1000), 463)
        self.assertEqual(int(position_pnl["gross"] / 1000), 463)
        self.assertEqual(int(position_pnl["lost"] / 1000), -458)
        self.assertEqual(position_pnl["trade_number"], 45)

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
        self.assertEqual(int(return_summary.total_return), 526)
        self.assertEqual(round(return_summary.annual_return, 1), 8.3)

        # test the sharpe ratio summary
        sharpe_ratio_summary = self.s.summary.sharpe_ratio_summary
        self.assertEqual(round(sharpe_ratio_summary.sharpe_ratio, 2), 0.66)

        # test the max draw down summary
        max_draw_down_summary = self.s.summary.max_draw_down_summary
        self.assertEqual(round(max_draw_down_summary.max_draw_down, 1), 36.8)

        # test the leverage ratio summary
        leverage_ratio_summary = self.s.summary.leverage_ratio_summary
        self.assertEqual(
            round(leverage_ratio_summary.leverage_ratio, 2),
            0.92)
