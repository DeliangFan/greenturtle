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

import unittest

from greenturtle.constants import varieties
from greenturtle.data.datafeed import mock
from greenturtle.backtesting import backtesting
from greenturtle.stragety import buyhold
from greenturtle.stragety import channel
from greenturtle.stragety import ema
from greenturtle.stragety import macd
from greenturtle.stragety import mim
from greenturtle.util.logging import logging


logger = logging.get_logger()
logger.disabled = True


# pylint: disable=R0801
class TestBasicFutureBacktrader(unittest.TestCase):
    """e2e test for future within backtrader."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.future_data = {}
        self.name = "mock"

    def setUp(self):
        self.s = backtesting.BackTesting(varieties=varieties.US_VARIETIES)

    def test_future_with_buy_and_hold(self):
        """test buy and hold future."""

        data = mock.get_mock_datafeed()
        self.s.add_data(data, self.name)
        self.s.add_strategy(buyhold.BuyHoldStrategy, risk_factor=0.1)
        self.s.do_backtesting()

        return_summary = self.s.summary.return_summary
        self.assertEqual(-3, int(return_summary.total_return))

    def test_future_with_ema(self):
        """test trade future with ema strategy."""

        data = mock.get_mock_datafeed()
        self.s.add_data(data, self.name)
        self.s.add_strategy(ema.EMA, risk_factor=0.1)
        self.s.do_backtesting()

        # test the return summary
        return_summary = self.s.summary.return_summary
        self.assertEqual(4, int(return_summary.total_return))
        self.assertEqual(6.2, round(return_summary.annual_return, 1))

    def test_future_with_mim(self):
        """test trade future with mim strategy."""

        data = mock.get_mock_datafeed()
        self.s.add_data(data, self.name)
        self.s.add_strategy(mim.MIMStrategy, risk_factor=0.1)
        self.s.do_backtesting()

        # test the return summary
        return_summary = self.s.summary.return_summary
        self.assertEqual(6, int(return_summary.total_return))
        self.assertEqual(7.9, round(return_summary.annual_return, 1))

    def test_future_with_channel(self):
        """test trade future with channel strategy."""

        data = mock.get_mock_datafeed()
        self.s.add_data(data, self.name)
        self.s.add_strategy(channel.DonchianChannel, risk_factor=0.1)
        self.s.do_backtesting()

        # test the return summary
        return_summary = self.s.summary.return_summary
        self.assertEqual(0, int(return_summary.total_return))
        self.assertEqual(0, round(return_summary.annual_return, 1))

    def test_future_with_macd(self):
        """test trade future with macd strategy."""

        data = mock.get_mock_datafeed()
        self.s.add_data(data, self.name)
        self.s.add_strategy(macd.MACDWithATRStrategy, risk_factor=0.1)
        self.s.do_backtesting()

        # test the return summary
        return_summary = self.s.summary.return_summary
        self.assertEqual(-8, int(return_summary.total_return))
        self.assertEqual(-11, round(return_summary.annual_return, 1))
