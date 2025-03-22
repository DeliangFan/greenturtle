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

"""unit tests for backtesting.py"""

import unittest

from greenturtle import exception
from greenturtle.backtesting import backtesting
from greenturtle.constants import varieties
from greenturtle.data.datafeed import mock
from greenturtle.stragety import ema
from greenturtle.util.logging import logging


logger = logging.get_logger()
logger.disabled = True


class TestFutureSimulator(unittest.TestCase):
    """unit tests for backtesting.py"""

    def test_get_auto_margin_success(self):
        """test get_auto_margin success"""
        b = backtesting.BackTesting(varieties=varieties.US_VARIETIES)
        ct_auto_margin = b.get_auto_margin("CT")
        self.assertEqual(50, ct_auto_margin)

        b = backtesting.BackTesting(varieties=varieties.CN_VARIETIES)
        cu_auto_margin = b.get_auto_margin("CU")
        self.assertEqual(0.5, cu_auto_margin)

    def test_get_auto_margin_failure(self):
        """test get_auto_margin failure"""
        b = backtesting.BackTesting(varieties=varieties.US_VARIETIES)
        self.assertRaises(
            exception.AutoMarginNotFound,
            b.get_auto_margin, "failure"
        )

        b = backtesting.BackTesting(varieties=varieties.CN_VARIETIES)
        self.assertRaises(
            exception.AutoMarginNotFound,
            b.get_auto_margin, "failure"
        )

    def test_get_multiplier_success(self):
        """test get_multiplier success"""
        b = backtesting.BackTesting(varieties=varieties.US_VARIETIES)
        ct_multiplier = b.get_multiplier("CT")
        self.assertEqual(500, ct_multiplier)

        b = backtesting.BackTesting(varieties=varieties.CN_VARIETIES)
        cu_multiplier = b.get_multiplier("CU")
        self.assertEqual(5, cu_multiplier)

    def test_get_multiplier_failure(self):
        """test get_multiplier failure"""
        b = backtesting.BackTesting(varieties=varieties.US_VARIETIES)
        self.assertRaises(
            exception.MultiplierNotFound,
            b.get_multiplier, "failure"
        )

        b = backtesting.BackTesting(varieties=varieties.CN_VARIETIES)
        self.assertRaises(
            exception.MultiplierNotFound,
            b.get_multiplier, "failure"
        )

    def test_set_commission_success(self):
        """test set_commission success"""
        b = backtesting.BackTesting(varieties=varieties.US_VARIETIES)
        b.set_commission(commission=4, name="GC")

    def test_set_default_commission_by_name_success(self):
        """test set_default_commission_by_name success"""
        b = backtesting.BackTesting(varieties=varieties.US_VARIETIES)
        b.set_default_commission_by_name("GC", 4)

    def test_do_backtesting(self):
        """test do_backtesting"""
        name = "mock"
        b = backtesting.BackTesting(varieties=varieties.US_VARIETIES)
        data = mock.get_mock_datafeed(name)
        b.add_data(data, name)
        b.add_strategy(ema.EMA, risk_factor=0.1)
        b.do_backtesting()

        # test the return summary
        return_summary = b.summary.return_summary
        self.assertEqual(4, int(return_summary.total_return))
        self.assertEqual(6.2, round(return_summary.annual_return, 1))

    def test_do_backtesting_with_commission(self):
        """test do_backtesting with commission"""
        name = "mock"
        b = backtesting.BackTesting(varieties=varieties.US_VARIETIES)
        data = mock.get_mock_datafeed(name)
        b.add_data(data, name)
        b.set_commission(commission=4, margin=5, mult=10, name=name)
        b.add_strategy(ema.EMA, risk_factor=0.1)
        b.do_backtesting()

        # test the return summary
        return_summary = b.summary.return_summary
        self.assertEqual(4, int(return_summary.total_return))
        self.assertEqual(5.5, round(return_summary.annual_return, 1))
