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

"""some basic e2e test for backtrader data"""

import datetime
import os
import unittest

from greenturtle.constants import types
from greenturtle.data.datafeed import csv
from greenturtle.data.datafeed import yf
from greenturtle.util.logging import logging


logging.set_log_error_level()


class TestFutureDataWithBackTrader(unittest.TestCase):
    """test greenturtle.data.backtrader.future file."""

    def setUp(self):
        """set up for each test case."""
        self.yahoo_code = "GC=F"
        self.name = "GC"
        self.filename = f"{self.name}.csv"

    def tearDown(self):
        """tear down for each test case."""
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_get_data_frame_from_yahoo_finance(self):
        """test get_data_frame_from_yahoo_finance"""
        df = yf.get_data_frame_from_yahoo_finance(self.yahoo_code)

        self.assertTrue(len(df) > 0)
        self.assertEqual(797, int(df.iloc[2000][types.CLOSE]))
        self.assertEqual(797, int(df.iloc[2000][types.ORI_CLOSE]))
        self.assertEqual(809, int(df.iloc[2000][types.ORI_HIGH]))
        self.assertEqual(794, int(df.iloc[2000][types.ORI_LOW]))
        self.assertEqual(801, int(df.iloc[2000][types.ORI_OPEN]))

    def test_get_data_frame_from_yahoo_finance_with_period(self):
        """test get_data_frame_from_yahoo_finance with period"""
        fromdate = datetime.datetime(2004, 1, 1)
        todate = datetime.datetime(2005, 1, 1)

        df = yf.get_data_frame_from_yahoo_finance(
            self.yahoo_code,
            fromdate=fromdate,
            todate=todate)

        self.assertEqual(249, len(df))

    def test_get_feed_from_yahoo_finance(self):
        """test get_feed_from_yahoo_finance"""
        df = yf.get_data_frame_from_yahoo_finance(
            self.yahoo_code)

        df.to_csv(self.filename)

        data = csv.get_feed_from_csv_file(
            self.name,
            self.filename)
        data.start()

        # TODO(fixme), provide better e2e test assert.
        self.assertIsNotNone(data)
        data.f.close()
