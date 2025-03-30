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

"""unittest for server.py"""

import unittest
from unittest import mock

import munch

from greenturtle.server import server


class TestServer(unittest.TestCase):
    """unittest for server.py"""

    def test_heartbeat(self):
        """test heartbeat"""
        conf = munch.Munch()
        conf.notifier = munch.Munch()
        s = server.Server(conf,
                          dbapi=mock.MagicMock(),
                          delta_data_syncer=mock.MagicMock())
        s.heartbeat()

    def test_trading(self):
        """test trading"""
        conf = munch.Munch()
        conf.notifier = munch.Munch()
        s = server.Server(conf,
                          dbapi=mock.MagicMock(),
                          delta_data_syncer=mock.MagicMock())
        s.trading(sleep_time=0)
