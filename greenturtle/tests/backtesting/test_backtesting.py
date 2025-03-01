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


class TestFutureSimulator(unittest.TestCase):
    """unit tests for backtesting.py"""

    def test_get_auto_margin_success(self):
        """test get_auto_margin success"""
        f = backtesting.BackTesting(varieties=varieties.US_VARIETIES)
        ct_auto_margin = f.get_auto_margin("CT")
        self.assertEqual(50, ct_auto_margin)

        f = backtesting.BackTesting(varieties=varieties.CN_VARIETIES)
        cu_auto_margin = f.get_auto_margin("CU")
        self.assertEqual(0.5, cu_auto_margin)

    def test_get_auto_margin_failure(self):
        """test get_auto_margin failure"""
        f = backtesting.BackTesting(varieties=varieties.US_VARIETIES)
        self.assertRaises(
            exception.AutoMarginNotFound,
            f.get_auto_margin, "failure"
        )

        f = backtesting.BackTesting(varieties=varieties.CN_VARIETIES)
        self.assertRaises(
            exception.AutoMarginNotFound,
            f.get_auto_margin, "failure"
        )

    def test_get_multiplier_success(self):
        """test get_multiplier success"""
        f = backtesting.BackTesting(varieties=varieties.US_VARIETIES)
        ct_multiplier = f.get_multiplier("CT")
        self.assertEqual(500, ct_multiplier)

        f = backtesting.BackTesting(varieties=varieties.CN_VARIETIES)
        cu_multiplier = f.get_multiplier("CU")
        self.assertEqual(5, cu_multiplier)

    def test_get_multiplier_failure(self):
        """test get_multiplier failure"""
        f = backtesting.BackTesting(varieties=varieties.US_VARIETIES)
        self.assertRaises(
            exception.MultiplierNotFound,
            f.get_multiplier, "failure"
        )

        f = backtesting.BackTesting(varieties=varieties.CN_VARIETIES)
        self.assertRaises(
            exception.MultiplierNotFound,
            f.get_multiplier, "failure"
        )

    def test_set_commission_success(self):
        """test set_commission success"""
        f = backtesting.BackTesting(varieties=varieties.US_VARIETIES)
        f.set_commission(commission=4, name="GC")

    def test_set_default_commission_by_name_success(self):
        """test set_default_commission_by_name success"""
        f = backtesting.BackTesting(varieties=varieties.US_VARIETIES)
        f.set_default_commission_by_name("GC", 4)
