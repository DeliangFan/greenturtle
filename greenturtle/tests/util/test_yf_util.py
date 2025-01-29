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

"""unit tests for yf_util.py"""

import unittest

import greenturtle.constants.stock as stock_const
from greenturtle.util import yf_util


class TestYFUtil(unittest.TestCase):
    """unit tests for yf_util.py"""

    def test_download_with_max_period(self):
        """test download_with_max_period"""
        df = yf_util.download_with_max_period(stock_const.TLT)
        self.assertEqual(round(df.iat[0, 0], 3), 38.279)

    def test_transform(self):
        """test transform"""
        df = yf_util.download_with_max_period(stock_const.TLT)
        df = yf_util.transform(df, stock_const.TLT)
        self.assertEqual(round(df["adj_close"].iloc[0], 3), 38.279)
