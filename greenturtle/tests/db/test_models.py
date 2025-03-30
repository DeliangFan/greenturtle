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

"""unittest for models.py"""

import unittest

from greenturtle.db import models


class TestContractModel(unittest.TestCase):
    """unittest for Contract model"""

    def test_columns(self):
        """test columns"""
        actual = []
        for name, table in models.Contract.metadata.tables.items():
            if name != models.Contract.__tablename__:
                continue
            for column in table.columns:
                actual.append(column.name)
        actual.sort()

        expect = [
            "close",
            "country",
            "created_at",
            "date",
            "exchange",
            "expire",
            "group",
            "high",
            "id",
            "low",
            "name",
            "open",
            "open_interest",
            "pre_settle",
            "settle",
            "source",
            "total_open_interest",
            "total_volume",
            "turn_over",
            "updated_at",
            "variety",
            "volume",
        ]

        self.assertEqual(expect, actual)


class TestContinuousModel(unittest.TestCase):
    """unittest for Continuous model"""

    def test_columns(self):
        """test columns"""
        actual = []
        for name, table in models.ContinuousContract.metadata.tables.items():
            if name != models.ContinuousContract.__tablename__:
                continue
            for column in table.columns:
                actual.append(column.name)
        actual.sort()

        expect = [
            "adjust_factor",
            "close",
            "country",
            "created_at",
            "date",
            "exchange",
            "expire",
            "group",
            "high",
            "id",
            "low",
            "name",
            "open",
            "open_interest",
            "pre_settle",
            "settle",
            "source",
            "total_open_interest",
            "total_volume",
            "turn_over",
            "updated_at",
            "variety",
            "volume",
        ]

        self.assertEqual(expect, actual)
