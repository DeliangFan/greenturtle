#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
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

"""analyzer the pnl for different positions."""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)


from backtrader import Analyzer


def do_notify_trade(position_pln, trade):
    """do_notify_trade deal with the notify trade"""

    position_pln["net"] += trade.pnlcomm
    position_pln["gross"] += trade.pnl
    position_pln["trade_number"] += 1

    if trade.pnlcomm >= 0.0:
        position_pln["profit"] += trade.pnlcomm
    else:
        position_pln["lost"] += trade.pnlcomm

    return position_pln


class PositionPNL(Analyzer):
    """
    Provides statistics on closed trades (keeps also the count of open ones)
    for all the positions.
      - ProfitAndLoss Total/Average break down in positions.
    """

    def notify_trade(self, trade):
        """deal with the notify trade"""
        # Trade just closed
        if trade.status != trade.Closed:
            return

        name = trade.getdataname()

        if name in self.rets:
            position_pln = self.rets[name]
        else:
            position_pln = {
                "lost": 0.0,
                "profit": 0.0,
                "net": 0.0,
                "gross": 0.0,
                "trade_number": 0
            }

        self.rets[name] = do_notify_trade(position_pln, trade)
