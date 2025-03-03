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

from greenturtle.brokers import tqbroker
from greenturtle import exception


class TestSymbolConvert(unittest.TestCase):
    """unit tests for tqbroker.py"""

    def setUp(self):
        """setup the convert"""
        self.convert = tqbroker.SymbolConvert(None)

    def test_tq_symbol_2_db_symbol_success(self):
        """test tq_symbol_2_db_symbol success"""
        self.assertEqual(
            "pg2602",
            self.convert.tq_symbol_2_db_symbol("pg2602", "DCE"))
        self.assertEqual(
            "SP2601",
            self.convert.tq_symbol_2_db_symbol("sp2601", "SHFE"))
        self.assertEqual(
            "UR601",
            self.convert.tq_symbol_2_db_symbol("UR601", "CZCE"))
        self.assertEqual(
            "IF2504",
            self.convert.tq_symbol_2_db_symbol("IF2504", "CFFEX"))
        self.assertEqual(
            "SC2601",
            self.convert.tq_symbol_2_db_symbol("sc2601", "INE"))
        self.assertEqual(
            "SI2601",
            self.convert.tq_symbol_2_db_symbol("si2601", "GFEX"))

    def test_tq_symbol_2_db_symbol_failed(self):
        """test tq_symbol_2_db_symbol failed"""
        self.assertRaises(
            exception.ExchangeNotSupportedError,
            self.convert.tq_symbol_2_db_symbol,
            "pg2602", "xxx")
        self.assertRaises(
            exception.ExchangeNotSupportedError,
            self.convert.tq_symbol_2_db_symbol,
            "SP2601", "SHFaE")

    def test_db_symbol_2_tq_symbol_success(self):
        """test db_symbol_2_tq_symbol success"""
        self.assertEqual(
            "pg2602",
            self.convert.db_symbol_2_tq_symbol("pg2602", "DCE"))
        self.assertEqual(
            "sp2601",
            self.convert.db_symbol_2_tq_symbol("SP2601", "SHFE"))
        self.assertEqual(
            "UR601",
            self.convert.db_symbol_2_tq_symbol("UR601", "CZCE"))
        self.assertEqual(
            "IF2504",
            self.convert.db_symbol_2_tq_symbol("IF2504", "CFFEX"))
        self.assertEqual(
            "sc2601",
            self.convert.db_symbol_2_tq_symbol("SC2601", "INE"))
        self.assertEqual(
            "si2601",
            self.convert.db_symbol_2_tq_symbol("SI2601", "GFEX"))

    def test_db_symbol_2_tq_symbol_failed(self):
        """test db_symbol_2_tq_symbol failed"""
        self.assertRaises(
            exception.ExchangeNotSupportedError,
            self.convert.db_symbol_2_tq_symbol,
            "pg2602", "xxx")
        self.assertRaises(
            exception.ExchangeNotSupportedError,
            self.convert.db_symbol_2_tq_symbol,
            "SP2601", "SHFaE")
