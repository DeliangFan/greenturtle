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

"""some utility functions"""

import pandas as pd


def nan2none(row):
    """convert pandas nan to None type."""
    new_row = row.copy()
    for k, v in row.items():
        new_row[k] = None if pd.isnull(v) else v
    return new_row


def emptystring2none(row):
    """convert pandas empty string to None type."""
    new_row = row.copy()
    for k, v in row.items():
        new_row[k] = None if v == "" else v
    return new_row


def get_group(variety, varieties):
    """get group name by variety name"""
    for group_name, group in varieties.items():
        for variety_name in group:
            if variety_name == variety:
                return group_name
    return None
