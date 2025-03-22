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


"""unittest for summary.py"""

import unittest

from greenturtle.analyzers import summary


class TestReturnSummary(unittest.TestCase):
    """test ReturnSummary"""

    def test_to_string(self):
        """test to_string function"""
        total_return = 699.89
        s = summary.ReturnSummary(total_return=total_return)
        first = '********** return summary **********\ntotal Return: 699.89%\n'
        self.assertEqual(first, s.to_string())


class TestSharpeRatioSummary(unittest.TestCase):
    """test SharpeRatioSummary"""

    def test_to_string(self):
        """test to_string function"""
        sharpe_ratio = 0.89
        s = summary.SharpeRatioSummary(sharpe_ratio=sharpe_ratio)
        first = ("********** sharpe ratio summary **********" +
                 "\nSharpe Ratio: 0.890\n")
        self.assertEqual(first, s.to_string())


class TestMaxDrawDownSummary(unittest.TestCase):
    """test MaxDrawDownSummary"""

    def test_to_string(self):
        """test to_string function"""
        max_draw_down = 28.1
        s = summary.MaxDrawDownSummary(max_draw_down=max_draw_down)
        first = ("********** max draw down summary **********\n" +
                 "Max Draw Down: 28.1%\n")
        self.assertEqual(first, s.to_string())


class TestLeverageRatioSummary(unittest.TestCase):
    """test LeverageRatioSummary"""

    def test_to_string(self):
        """test to_string function"""
        leverage_ratio = 30.1
        s = summary.LeverageRatioSummary(leverage_ratio=leverage_ratio)
        first = ("********** leverage ratio summary **********\n" +
                 "leverage ratio: 30.10\n")
        self.assertEqual(first, s.to_string())


class TestPositionsPNLSummary(unittest.TestCase):
    """test PositionsPNLSummary"""

    def test_to_string(self):
        """test to_string function"""
        positions_pnl = {
            "IF":  {
                "net": 10000,
                "profit": 20000,
                "lost": 10000,
                "gross": 10002,
                "trade_number": 10,
            },
        }
        s = summary.PositionsPNLSummary(positions_pnl)
        first = ("********** trade summary **********\n" +
                 "IF, net: 10000, profit: 20000, lost: 10000, " +
                 "comm: 2, trader number: 10\n")
        self.assertEqual(first, s.to_string())


class TestSummary(unittest.TestCase):
    """test Summary"""

    def test_to_string(self):
        """test to_string function"""
        total_return = 699.89
        s = summary.Summary()
        s.return_summary = summary.ReturnSummary(total_return=total_return)

        first = ("\n********** return summary **********\n" +
                 "total Return: 699.89%\n")

        self.assertEqual(first, s.to_string())
