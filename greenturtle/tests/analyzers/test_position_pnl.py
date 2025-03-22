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

"""unittest for position_pnl.py"""


import unittest

from backtrader import trade

from greenturtle.analyzers import position_pnl


class TestDoNotifyTrade(unittest.TestCase):
    """unittest for position_pnl.py"""

    def test_do_notify_trade(self):
        """test do_notify_trade"""
        t = trade.Trade()
        t.pnlcomm = 10
        t.pnl = 11

        pln = {
            "profit": 0.0,
            "lost": 0.0,
            "gross": 0.0,
            "net": 0.0,
            "trade_number": 0
        }

        pln = position_pnl.do_notify_trade(pln, t)

        self.assertEqual(11, pln["gross"])
        self.assertEqual(10, pln["net"])
        self.assertEqual(1, pln["trade_number"])

        pln = position_pnl.do_notify_trade(pln, t)

        self.assertEqual(22, pln["gross"])
        self.assertEqual(20, pln["net"])
        self.assertEqual(2, pln["trade_number"])
