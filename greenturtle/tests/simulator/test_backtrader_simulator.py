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

"""unit tests for simulator.py"""

import unittest

from greenturtle.data.backtrader import future
from greenturtle.simulator.backtrader import simulator
from greenturtle.stragety.backtrader import ema


class TestSimulator(unittest.TestCase):
    """unit tests for simulator.py"""

    def test_without_run(self):
        """test with no run"""
        s = simulator.Simulator()
        s.add_strategy(ema.EMA)
        fake_data = future.get_feed_from_csv_file("fake", "fake_filename")
        s.add_data(fake_data, "fake")
