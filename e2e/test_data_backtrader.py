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

"""some basic e2e test for stock"""

import datetime
import os
import unittest

import pandas as pd

import greenturtle.constants as const
import greenturtle.data.backtrader.stock as stock_data
import greenturtle.data.backtrader.future as future_data
import greenturtle.data.backtrader.crypto as crypto_data
from greenturtle.util.logging import logging


logging.set_log_error_level()


class TestStockDataWithBackTrader(unittest.TestCase):
    """test greenturtle.data.backtrader.stock file."""

    def test_get_feed_from_yahoo_finance_with_max_period(self):
        """test get_feed_from_yahoo_finance with max period"""
        name = "TLT"

        data = stock_data.get_feed_from_yahoo_finance(name)

        # pylint: disable=no-member
        length = len(data.p.dataname)
        self.assertTrue(length > 0)

    def test_get_feed_from_yahoo_finance_with_period(self):
        """test get_feed_from_yahoo_finance with period"""

        name = "QQQ"
        fromdate = datetime.datetime(2004, 1, 1)
        todate = datetime.datetime(2005, 1, 1)

        data = stock_data.get_feed_from_yahoo_finance(
            name,
            fromdate=fromdate,
            todate=todate)

        # pylint: disable=no-member
        length = len(data.p.dataname)
        self.assertEqual(252, length)


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
        df = future_data.get_data_frame_from_yahoo_finance(self.yahoo_code)

        self.assertTrue(len(df) > 0)
        self.assertEqual(797, int(df.iloc[2000][const.CLOSE]))
        self.assertEqual(797, int(df.iloc[2000][const.ORI_CLOSE]))
        self.assertEqual(809, int(df.iloc[2000][const.ORI_HIGH]))
        self.assertEqual(794, int(df.iloc[2000][const.ORI_LOW]))
        self.assertEqual(801, int(df.iloc[2000][const.ORI_OPEN]))

    def test_get_data_frame_from_yahoo_finance_with_period(self):
        """test get_data_frame_from_yahoo_finance with period"""
        fromdate = datetime.datetime(2004, 1, 1)
        todate = datetime.datetime(2005, 1, 1)

        df = future_data.get_data_frame_from_yahoo_finance(
            self.yahoo_code,
            fromdate=fromdate,
            todate=todate)

        self.assertEqual(249, len(df))

    def test_get_feed_from_yahoo_finance(self):
        """test get_feed_from_yahoo_finance"""
        df = future_data.get_data_frame_from_yahoo_finance(
            self.yahoo_code)

        df.to_csv(self.filename)

        data = future_data.get_feed_from_csv_file(
            self.name,
            self.filename)
        data.start()

        # TODO(fixme), provide better e2e test assert.
        self.assertIsNotNone(data)
        data.f.close()


class TestCryptoDataWithBackTrader(unittest.TestCase):
    """test greenturtle.data.backtrader.crypto file."""

    def setUp(self):
        """set up for each test case."""
        self.name = "BTC"
        self.filename = f"{self.name}.csv"
        data = {
            "datatime": [datetime.datetime(2004, 1, 1)],
            "open": 10,
            "high": 12,
            "low": 8,
            "close": 9,
            "volume": 100,
        }
        df = pd.DataFrame(data)
        df.to_csv(self.filename)

    def tearDown(self):
        """tear down for each test case."""

        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_get_feed_from_csv_file(self):
        """test get_feed_from_csv_file."""

        data = crypto_data.get_feed_from_csv_file(self.name, self.filename)
        data.start()

        # TODO(fixme), provide better e2e test assert.
        self.assertIsNotNone(data)
        data.f.close()
