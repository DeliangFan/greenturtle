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

import greenturtle.constants.future as future_const
import greenturtle.data.backtrader.future as future_data
from greenturtle.simulator.backtrader import simulator
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
        self.fromdate = datetime(2000, 1, 1)
        self.todate = datetime(2024, 1, 1)

        for category_name, category_value in future_const.FUTURE.items():
            for name, future in category_value.items():

                # pylint: disable=invalid-name
                yahoo_code = future[future_const.YAHOO_CODE]
                contract_unit = future[future_const.CONTRACT_UNIT]
                margin_requirement_ratio = \
                    future[future_const.MARGIN_REQUIREMENT_RATIO]

                # get feed data from yahoo finance
                data = future_data.get_feed_from_yahoo_finance(
                    yahoo_code,
                    name=name,
                    category=category_name,
                    contract_unit=contract_unit,
                    margin_requirement_ratio=margin_requirement_ratio,
                    fromdate=self.fromdate,
                    todate=self.todate)

                self.future_data[name] = data

    def setUp(self):
        self.s = simulator.Simulator(commission=0, slippage=0)

    def test_future_with_buy_and_hold(self):
        """test buy and hold future."""

        name = "HG"
        data = self.future_data[name]
        self.s.add_data(data, name)
        self.s.add_strategy(buyhold.BuyHoldStrategy)
        self.s.do_simulate()

        return_summary = self.s.summary.return_summary
        self.assertEqual(314, int(return_summary.total_return))
        self.assertEqual(6.3, round(return_summary.annual_return, 1))

        sharpe_ratio_summary = self.s.summary.sharpe_ratio_summary
        self.assertEqual(0.29, round(sharpe_ratio_summary.sharpe_ratio, 2))

        max_draw_down_summary = self.s.summary.max_draw_down_summary
        self.assertEqual(68.3, round(max_draw_down_summary.max_draw_down, 1))

        leverage_ratio_summary = self.s.summary.leverage_ratio_summary
        self.assertEqual(0.97,
                         round(leverage_ratio_summary.leverage_ratio, 2))

    def test_future_with_ema(self):
        """test trade future with ema strategy."""

        name = "HG"
        data = self.future_data[name]
        self.s.add_data(data, name)
        self.s.add_strategy(ema.EMA)
        self.s.do_simulate()

        # test the return summary
        return_summary = self.s.summary.return_summary
        self.assertEqual(308, int(return_summary.total_return))
        self.assertEqual(6.2, round(return_summary.annual_return, 1))

        # test the sharpe ratio summary
        sharpe_ratio_summary = self.s.summary.sharpe_ratio_summary
        self.assertEqual(0.32, round(sharpe_ratio_summary.sharpe_ratio, 2))

        # test the max draw down summary
        max_draw_down_summary = self.s.summary.max_draw_down_summary
        self.assertEqual(54.2, round(max_draw_down_summary.max_draw_down, 1))

        # test the leverage ratio summary
        leverage_ratio_summary = self.s.summary.leverage_ratio_summary
        self.assertEqual(
            0.53,
            round(leverage_ratio_summary.leverage_ratio, 2))

        # test the trade summary
        trade_summary = self.s.summary.trade_summary
        self.assertEqual(2983, int(trade_summary.net / 1000))
        self.assertEqual(2983, int(trade_summary.gross / 1000))
        self.assertEqual(8730, int(trade_summary.won / 1000))
        self.assertEqual(-5747, int(trade_summary.lost / 1000))
        self.assertEqual(56, trade_summary.trader_number)
        self.assertEqual(11, trade_summary.win_trader_number)

        # test the position profit and lost summary
        positions_pnl_summary = self.s.summary.positions_pnl_summary
        positions_pnl = positions_pnl_summary.positions_pnl
        self.assertIn(name, positions_pnl)

        position_pnl = positions_pnl[name]
        self.assertEqual(2983, int(position_pnl["net"] / 1000))
        self.assertEqual(2983, int(position_pnl["gross"] / 1000))
        self.assertEqual(-5747, int(position_pnl["lost"] / 1000))
        self.assertEqual(55, position_pnl["trade_number"])

    def test_future_with_mim(self):
        """test trade future with mim strategy."""

        name = "HG"
        data = self.future_data[name]
        self.s.add_data(data, name)
        self.s.add_strategy(mim.MIMStrategy)
        self.s.do_simulate()

        # test the return summary
        return_summary = self.s.summary.return_summary
        self.assertEqual(319, int(return_summary.total_return))
        self.assertEqual(6.4, round(return_summary.annual_return, 1))

        # test the sharpe ratio summary
        sharpe_ratio_summary = self.s.summary.sharpe_ratio_summary
        self.assertEqual(0.32, round(sharpe_ratio_summary.sharpe_ratio, 2))

        # test the max draw down summary
        max_draw_down_summary = self.s.summary.max_draw_down_summary
        self.assertEqual(47.3, round(max_draw_down_summary.max_draw_down, 1))

        # test the leverage ratio summary
        leverage_ratio_summary = self.s.summary.leverage_ratio_summary
        self.assertEqual(
            0.52,
            round(leverage_ratio_summary.leverage_ratio, 2))

        # test the trade summary
        trade_summary = self.s.summary.trade_summary
        self.assertEqual(3100, int(trade_summary.net / 1000))
        self.assertEqual(3100, int(trade_summary.gross / 1000))
        self.assertEqual(10554, int(trade_summary.won / 1000))
        self.assertEqual(-7453, int(trade_summary.lost / 1000))
        self.assertEqual(173, trade_summary.trader_number)
        self.assertEqual(49, trade_summary.win_trader_number)

        # test the position profit and lost summary
        positions_pnl_summary = self.s.summary.positions_pnl_summary
        positions_pnl = positions_pnl_summary.positions_pnl
        self.assertIn(name, positions_pnl)

        position_pnl = positions_pnl[name]
        self.assertEqual(3100, int(position_pnl["net"] / 1000))
        self.assertEqual(3100, int(position_pnl["gross"] / 1000))
        self.assertEqual(-7453, int(position_pnl["lost"] / 1000))
        self.assertEqual(172, position_pnl["trade_number"])

    def test_future_with_channel(self):
        """test trade future with channel strategy."""

        name = "HG"
        data = self.future_data[name]
        self.s.add_data(data, name)
        self.s.add_strategy(channel.DonchianChannel)
        self.s.do_simulate()

        # test the return summary
        return_summary = self.s.summary.return_summary
        self.assertEqual(-4, int(return_summary.total_return))
        self.assertEqual(-0.2, round(return_summary.annual_return, 1))

        # test the sharpe ratio summary
        sharpe_ratio_summary = self.s.summary.sharpe_ratio_summary
        self.assertEqual(-0.14, round(sharpe_ratio_summary.sharpe_ratio, 2))

        # test the max draw down summary
        max_draw_down_summary = self.s.summary.max_draw_down_summary
        self.assertEqual(30.3, round(max_draw_down_summary.max_draw_down, 1))

        # test the leverage ratio summary
        leverage_ratio_summary = self.s.summary.leverage_ratio_summary
        self.assertEqual(
            0.06,
            round(leverage_ratio_summary.leverage_ratio, 2))

        # test the trade summary
        trade_summary = self.s.summary.trade_summary
        self.assertEqual(-49, int(trade_summary.net / 1000))
        self.assertEqual(-49, int(trade_summary.gross / 1000))
        self.assertEqual(1293, int(trade_summary.won / 1000))
        self.assertEqual(-1343, int(trade_summary.lost / 1000))
        self.assertEqual(209, trade_summary.trader_number)
        self.assertEqual(95, trade_summary.win_trader_number)

        # test the position profit and lost summary
        positions_pnl_summary = self.s.summary.positions_pnl_summary
        positions_pnl = positions_pnl_summary.positions_pnl
        self.assertIn(name, positions_pnl)

        position_pnl = positions_pnl[name]
        self.assertEqual(-49, int(position_pnl["net"] / 1000))
        self.assertEqual(-49, int(position_pnl["gross"] / 1000))
        self.assertEqual(-1343, int(position_pnl["lost"] / 1000))
        self.assertEqual(209, position_pnl["trade_number"])

    def test_future_with_macd(self):
        """test trade future with macd strategy."""

        name = "HG"
        data = self.future_data[name]
        self.s.add_data(data, name)
        self.s.add_strategy(macd.MACDWithATRStrategy)
        self.s.do_simulate()

        # test the return summary
        return_summary = self.s.summary.return_summary
        self.assertEqual(7, int(return_summary.total_return))
        self.assertEqual(0.3, round(return_summary.annual_return, 1))

        # test the sharpe ratio summary
        sharpe_ratio_summary = self.s.summary.sharpe_ratio_summary
        self.assertEqual(-0.22, round(sharpe_ratio_summary.sharpe_ratio, 2))

        # test the max draw down summary
        max_draw_down_summary = self.s.summary.max_draw_down_summary
        self.assertEqual(11.8, round(max_draw_down_summary.max_draw_down, 1))

        # test the leverage ratio summary
        leverage_ratio_summary = self.s.summary.leverage_ratio_summary
        self.assertEqual(
            0.02,
            round(leverage_ratio_summary.leverage_ratio, 2))

        # test the trade summary
        trade_summary = self.s.summary.trade_summary
        self.assertEqual(73, int(trade_summary.net / 1000))
        self.assertEqual(73, int(trade_summary.gross / 1000))
        self.assertEqual(676, int(trade_summary.won / 1000))
        self.assertEqual(-602, int(trade_summary.lost / 1000))
        self.assertEqual(131, trade_summary.trader_number)
        self.assertEqual(70, trade_summary.win_trader_number)

        # test the position profit and lost summary
        positions_pnl_summary = self.s.summary.positions_pnl_summary
        positions_pnl = positions_pnl_summary.positions_pnl
        self.assertIn(name, positions_pnl)

        position_pnl = positions_pnl[name]
        self.assertEqual(73, int(position_pnl["net"] / 1000))
        self.assertEqual(73, int(position_pnl["gross"] / 1000))
        self.assertEqual(-602, int(position_pnl["lost"] / 1000))
        self.assertEqual(131, position_pnl["trade_number"])

    def test_future_with_rsi(self):
        """test trade future with rsi strategy."""

        name = "HG"
        data = self.future_data[name]
        self.s.add_data(data, name)
        self.s.add_strategy(rsi.RSIStrategy)
        self.s.do_simulate()

        # test the return summary
        return_summary = self.s.summary.return_summary
        self.assertEqual(1, int(return_summary.total_return))
        self.assertEqual(0.1, round(return_summary.annual_return, 1))

        # test the sharpe ratio summary
        sharpe_ratio_summary = self.s.summary.sharpe_ratio_summary
        self.assertEqual(-0.26, round(sharpe_ratio_summary.sharpe_ratio, 2))

        # test the max draw down summary
        max_draw_down_summary = self.s.summary.max_draw_down_summary
        self.assertEqual(25.9, round(max_draw_down_summary.max_draw_down, 1))

        # test the leverage ratio summary
        leverage_ratio_summary = self.s.summary.leverage_ratio_summary
        self.assertEqual(
            0.03,
            round(leverage_ratio_summary.leverage_ratio, 2))

        # test the trade summary
        trade_summary = self.s.summary.trade_summary
        self.assertEqual(12, int(trade_summary.net / 1000))
        self.assertEqual(12, int(trade_summary.gross / 1000))
        self.assertEqual(691, int(trade_summary.won / 1000))
        self.assertEqual(-678, int(trade_summary.lost / 1000))
        self.assertEqual(63, trade_summary.trader_number)
        self.assertEqual(44, trade_summary.win_trader_number)

        # test the position profit and lost summary
        positions_pnl_summary = self.s.summary.positions_pnl_summary
        positions_pnl = positions_pnl_summary.positions_pnl
        self.assertIn(name, positions_pnl)

        position_pnl = positions_pnl[name]
        self.assertEqual(12, int(position_pnl["net"] / 1000))
        self.assertEqual(12, int(position_pnl["gross"] / 1000))
        self.assertEqual(-678, int(position_pnl["lost"] / 1000))
        self.assertEqual(63, position_pnl["trade_number"])
