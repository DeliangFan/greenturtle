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

"""data transform for csv, db, datafeed etc"""

import pandas as pd

from greenturtle.db import models


def pd_row_nan_2_none(row):
    """convert pandas nan to None type."""
    new_row = row.copy()
    for k, v in row.items():
        new_row[k] = None if pd.isnull(v) else v
    return new_row


def pd_row_emptystring_2_none(row):
    """convert pandas empty string to None type."""
    new_row = row.copy()
    for k, v in row.items():
        new_row[k] = None if v == "" else v
    return new_row


def contract_model_2_dataframe(model):
    """contract model to pandas dataframe."""
    attr_dict = model.to_dict()
    df = pd.DataFrame([attr_dict])
    return df


def contract_dataframe_2_model():
    """contract dataframe tp model class."""
    raise NotImplementedError("contract dataframe_2_model not implemented.")


def contract_model_2_continuous_contract_model(contract):
    """contract model to continuous_contract_model."""
    attr_dict = contract.to_dict()
    continuous_contract = models.ContinuousContract()
    continuous_contract.update(attr_dict)
    continuous_contract.adjust_factor = 1
    return continuous_contract
