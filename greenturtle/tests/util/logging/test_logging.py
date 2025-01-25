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

"""unit tests for logging.py"""

import unittest

from greenturtle.util.logging import logging


class TestLogging(unittest.TestCase):
    """unit tests for logging.py"""

    def test_logging_name(self):
        """test logging name."""
        logger = logging.get_logger()
        self.assertEqual(logger.name, logging.LOGGER_NAME)

    def test_logging_handler(self):
        """test logging handler."""
        logger = logging.get_logger()
        self.assertTrue(logger.hasHandlers)

        handlers = logger.handlers
        self.assertTrue(len(handlers) == 2)

    def test_logging_works(self):
        """test logging works."""
        logger = logging.get_logger()
        logger.info("logging info.")
        self.assertTrue(logger.hasHandlers)
