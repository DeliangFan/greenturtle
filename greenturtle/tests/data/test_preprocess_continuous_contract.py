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

"""unittest for continuous_contract.py"""

import datetime
import unittest

from greenturtle.db import models
from greenturtle.data.preprocess import continuous_contract


class TestContinuousContract(unittest.TestCase):
    """test cases for ContinuousContract"""

    def test_get_sorted_dates(self):
        """test get_sorted_dates"""
        c1 = models.Contract(date=datetime.datetime(2025, 3, 26))
        c2 = models.Contract(date=datetime.datetime(2025, 3, 24))
        c3 = models.Contract(date=datetime.datetime(2025, 3, 25))

        func = continuous_contract.DeltaContinuousContract.get_sorted_dates
        actual = func([c1, c2, c3])
        expect = [
            datetime.datetime(2025, 3, 24),
            datetime.datetime(2025, 3, 25),
            datetime.datetime(2025, 3, 26),
        ]
        self.assertEqual(expect, actual)
