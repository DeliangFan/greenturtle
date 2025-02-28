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

"""unit tests for validation.py"""

import unittest

from greenturtle import exception
from greenturtle.data import validation


class TestValidation(unittest.TestCase):
    """unit tests for validation.py"""

    def test_validate_positive_price_success(self):
        """test validate_positive_price success."""
        validation.validate_positive_price(100)
        validation.validate_positive_price(1)

    def test_validate_positive_price_failure(self):
        """test validate_positive_price failure."""
        self.assertRaises(
            exception.DataPriceNonPositiveError,
            validation.validate_positive_price,
            -1,
        )
        self.assertRaises(
            exception.DataPriceNonPositiveError,
            validation.validate_positive_price,
            0,
        )

    def test_validate_high_price_success(self):
        """test validate_high_price success."""
        validation.validate_high_price(100, 101, 99, 100)
        validation.validate_high_price(100, 100, 99, 100)

    def test_validate_high_price_failure(self):
        """test validate_high_price failure."""
        self.assertRaises(
            exception.DataPriceHighAbnormalError,
            validation.validate_high_price, 100, 99, 98, 100)
        self.assertRaises(
            exception.DataPriceHighAbnormalError,
            validation.validate_high_price, 99, 99, 98, 100)

    def test_validate_low_price_success(self):
        """test validate_low_price success."""
        validation.validate_high_price(100, 101, 99, 100)
        validation.validate_high_price(100, 100, 99, 100)

    def test_validate_low_price_failure(self):
        """test validate_low_price failure."""
        self.assertRaises(
            exception.DataPriceLowAbnormalError,
            validation.validate_low_price, 100, 101, 99, 98
        )
        self.assertRaises(
            exception.DataPriceLowAbnormalError,
            validation.validate_low_price, 98, 101, 99, 100
        )

    def test_validate_price_type_failure(self):
        """test validate_price_type failure."""
        self.assertRaises(
            exception.DataPriceInvalidTypeError,
            validation.validate_price_type, None, 101, -1, 98
        )
        self.assertRaises(
            exception.DataPriceInvalidTypeError,
            validation.validate_price, 102, "", 98, 100
        )

    def test_validate_price_type_success(self):
        """test validate_price_type success."""
        validation.validate_high_price(100, 101, 99, 100)
        validation.validate_high_price(100.0, 100.1, 99, 100)

    def test_validate_price_success(self):
        """test validate_price success."""
        validation.validate_price(100, 101, 99, 100)

    def test_validate_price_failure(self):
        """test validate_price failure."""
        self.assertRaises(
            exception.DataPriceNonPositiveError,
            validation.validate_price, 100, 101, -1, 98
        )
        self.assertRaises(
            exception.DataPriceHighAbnormalError,
            validation.validate_price, 102, 101, 98, 100
        )
        self.assertRaises(
            exception.DataPriceLowAbnormalError,
            validation.validate_price, 100, 102, 99, 98
        )

    def test_validate_price_daily_limit(self):
        """"test validate_price_daily_limit."""
        self.assertRaises(
            exception.DataPriceExceedDailyLimitError,
            validation.validate_price_daily_limit,
            10, 5
        )

        validation.validate_price_daily_limit(10, 10.01)
