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

"""unittest for tq broker module"""

import unittest

from greenturtle.brokers import backbroker


class TestBackBroker(unittest.TestCase):
    """unittest class for backbroker module"""

    def test_account_overview(self):
        """test account_overview"""
        b = backbroker.BackBroker()
        second = b.account_overview()
        first = "Back broker: value: 1000000, cash: 1000000"
        self.assertEqual(first, second)
