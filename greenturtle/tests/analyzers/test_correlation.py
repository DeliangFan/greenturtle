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

"""unittest for correlation.py"""

import datetime
import unittest

import pandas as pd

from greenturtle.analyzers import correlation
from greenturtle.analyzers import summary


class TestCorrelation(unittest.TestCase):
    """unittest for correlation"""

    def test_correlation_with_same_sequence(self):
        """test correlation with same sequence"""
        days_return = {
            datetime.datetime(2002, 1, 1): 1,
            datetime.datetime(2002, 1, 2): 2,
            datetime.datetime(2002, 1, 3): 3,
            datetime.datetime(2002, 1, 4): 4,

        }
        s1 = summary.ReturnSummary(days_return=days_return)
        s2 = summary.ReturnSummary(days_return=days_return)

        c = correlation.Correlation()
        c.add_return_summary("s1", s1)
        c.add_return_summary("s2", s2)
        corr = c.compute_correlation()

        self.assertEqual(1, corr.iloc[0, 1])
        self.assertEqual(1, corr.iloc[0, 0])

    def test_correlation_with_zero_correlation(self):
        """test correlation with zero correlation"""

        days_return1 = {
            datetime.datetime(2002, 1, 1): 1,
            datetime.datetime(2002, 1, 2): 1,
            datetime.datetime(2002, 1, 3): 1,
            datetime.datetime(2002, 1, 4): 1,
        }

        days_return2 = {
            datetime.datetime(2002, 1, 1): 0,
            datetime.datetime(2002, 1, 2): 1,
            datetime.datetime(2002, 1, 3): 0,
            datetime.datetime(2002, 1, 4): 1,
        }

        s1 = summary.ReturnSummary(days_return=days_return1)
        s2 = summary.ReturnSummary(days_return=days_return2)

        c = correlation.Correlation()
        c.add_return_summary("s1", s1)
        c.add_return_summary("s2", s2)
        corr = c.compute_correlation()

        self.assertEqual(True, pd.isnull(corr.iloc[0, 1]))

    def test_correlation_with_negative_correlation(self):
        """test correlation with negative correlation"""

        days_return1 = {
            datetime.datetime(2002, 1, 1): 1,
            datetime.datetime(2002, 1, 2): 0,
            datetime.datetime(2002, 1, 3): 1,
            datetime.datetime(2002, 1, 4): 0,
        }

        days_return2 = {
            datetime.datetime(2002, 1, 1): 0,
            datetime.datetime(2002, 1, 2): 2,
            datetime.datetime(2002, 1, 3): 0,
            datetime.datetime(2002, 1, 4): 2,
        }

        s1 = summary.ReturnSummary(days_return=days_return1)
        s2 = summary.ReturnSummary(days_return=days_return2)

        c = correlation.Correlation()
        c.add_return_summary("s1", s1)
        c.add_return_summary("s2", s2)
        corr = c.compute_correlation()

        self.assertEqual(-1, corr.iloc[0, 1])

    def test_correlation_with_positive_correlation(self):
        """test correlation with positive correlation"""

        days_return1 = {
            datetime.datetime(2002, 1, 1): 1,
            datetime.datetime(2002, 1, 2): 2,
            datetime.datetime(2002, 1, 3): 4,
            datetime.datetime(2002, 1, 4): 8,
        }

        days_return2 = {
            datetime.datetime(2002, 1, 1): 1,
            datetime.datetime(2002, 1, 2): 2,
            datetime.datetime(2002, 1, 3): 3,
            datetime.datetime(2002, 1, 4): 9,
        }

        s1 = summary.ReturnSummary(days_return=days_return1)
        s2 = summary.ReturnSummary(days_return=days_return2)

        c = correlation.Correlation()
        c.add_return_summary("s1", s1)
        c.add_return_summary("s2", s2)
        corr = c.compute_correlation()

        self.assertEqual(1, corr.iloc[0, 1])

    def test_pearson_correlation_with_positive_correlation(self):
        """test pearson correlation with positive correlation"""

        days_return1 = {
            datetime.datetime(2002, 1, 1): 1,
            datetime.datetime(2002, 1, 2): 2,
            datetime.datetime(2002, 1, 3): 3,
            datetime.datetime(2002, 1, 4): 9,
        }

        days_return2 = {
            datetime.datetime(2002, 1, 1): 1,
            datetime.datetime(2002, 1, 2): 2,
            datetime.datetime(2002, 1, 3): 4,
            datetime.datetime(2002, 1, 4): 8,
        }

        s1 = summary.ReturnSummary(days_return=days_return1)
        s2 = summary.ReturnSummary(days_return=days_return2)

        c = correlation.Correlation()
        c.add_return_summary("s1", s1)
        c.add_return_summary("s2", s2)
        corr = c.compute_correlation(method="pearson")

        self.assertEqual(0.98, round(corr.iloc[0, 1], 2))
