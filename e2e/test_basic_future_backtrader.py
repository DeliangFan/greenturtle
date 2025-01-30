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
