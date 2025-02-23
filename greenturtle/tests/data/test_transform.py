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

"""unit tests for transform.py"""

import unittest

import numpy as np
import pandas as pd

from greenturtle import exception
from greenturtle.data import transform
from greenturtle.db import models


class TestValidation(unittest.TestCase):

    def test_contract_model_2_continuous_contract_model(self):
        """test pd_row_nan_2_none"""
        contract = models.Contract(name="myname")
        func = transform.contract_model_2_continuous_contract_model
        continuous_contract = func(contract)
        self.assertEqual("myname", continuous_contract.name)
        self.assertEqual(1, continuous_contract.adjust_factor)
        self.assertEqual(
            True,
            isinstance(continuous_contract,
                       models.ContinuousContract))

    def test_pd_row_emptystring_2_none(self):
        """test pd_row_emptystring_2_none"""
        df = pd.DataFrame([{"a": "xxx", "b": "xxx"}, {"a": "a", "b": ""}])
        for _, row in df.iterrows():
            actual = transform.pd_row_emptystring_2_none(row)
            if row.b == "":
                self.assertEqual(True, pd.isnull(actual.b))
