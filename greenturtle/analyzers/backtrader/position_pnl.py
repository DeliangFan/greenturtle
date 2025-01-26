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


class PositionPNL(Analyzer):
    """
    Provides statistics on closed trades (keeps also the count of open ones)
    for all the positions.
      - ProfitAndLoss Total/Average break down in positions.
    """

    def notify_trade(self, trade):

        if trade.status != trade.Closed:
            return

        # Trade just closed
        name = trade.getdataname()
        if name in self.rets:
            position_pln = self.rets[name]
        else:
            position_pln = {
                "lost": 0.0,
                "profit": 0.0,
                "net": 0.0,
                "gross": 0.0,
                "count": 0}

        position_pln["net"] += trade.pnlcomm
        position_pln["gross"] += trade.pnl
        position_pln["count"] += 1

        if trade.pnlcomm >= 0.0:
            position_pln["profit"] += trade.pnlcomm
        else:
            position_pln["lost"] += trade.pnlcomm

        self.rets[name] = position_pln
