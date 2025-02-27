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

"""unittest for calendar module"""

import datetime
import unittest

from greenturtle.util import calendar
from greenturtle import exception


class TestCalendar(unittest.TestCase):
    """unit tests for calendar.py"""

    def test_validate_cn_date_success(self):
        """test validate_cn_date success"""
        calendar.validate_cn_date(datetime.date(2010, 1, 1))
        calendar.validate_cn_date(datetime.date(2004, 1, 2))
        calendar.validate_cn_date(datetime.date(2025, 12, 31))

    def test_validate_cn_date_failed(self):
        """test validate_cn_date failed"""
        self.assertRaises(
            exception.ValidateTradingDayError,
            calendar.validate_cn_date,
            datetime.date(2003, 12, 31),
        )
        self.assertRaises(
            exception.ValidateTradingDayError,
            calendar.validate_cn_date,
            datetime.date(2026, 1, 1),
        )

    def test_is_cn_trading_day(self):
        """test is_cn_trading_day"""
        self.assertTrue(calendar.is_cn_trading_day(
            datetime.date(2019, 1, 2)))
        self.assertTrue(calendar.is_cn_trading_day(
            datetime.date(2025, 1, 27)))
        self.assertTrue(calendar.is_cn_trading_day(
            datetime.date(2025, 2, 28)))

        self.assertFalse(calendar.is_cn_trading_day(
            datetime.date(2025, 1, 26)))
        self.assertFalse(calendar.is_cn_trading_day(
            datetime.date(2025, 1, 28)))

        self.assertRaises(
            exception.ValidateTradingDayError,
            calendar.is_cn_trading_day,
            datetime.date(2003, 12, 31),
        )
        self.assertRaises(
            exception.ValidateTradingDayError,
            calendar.is_cn_trading_day,
            datetime.date(2026, 1, 1),
        )

    def test_get_cn_trading_days(self):
        """test get_cn_trading_days"""

        start_date = datetime.date(2025, 1, 26)
        end_date = datetime.date(2025, 1, 28)
        actual = calendar.get_cn_trading_days(start_date, end_date)
        expect = [datetime.date(2025, 1, 27)]
        self.assertEqual(expect, actual)

        end_date = datetime.date(2026, 1, 1)
        self.assertRaises(
            exception.ValidateTradingDayError,
            calendar.get_cn_trading_days,
            start_date, end_date,
        )
