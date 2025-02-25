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

"""Generate aligned continuous files from continuous file."""

import copy
import os

import pandas as pd

from greenturtle.constants import types


class Align:
    """Align the varieties contracts with time."""

    def __init__(self, varieties_path, dst_dir):
        self.varieties_path = varieties_path
        self.dst_dir = dst_dir

    @staticmethod
    def load_one(file_path):
        """load one variety from csv file."""
        names = [types.DATETIME] + types.CONTINUOUS_COLUMN
        df = pd.read_csv(
            file_path,
            index_col=types.DATETIME,
            names=names,
            dtype=types.CONTINUOUS_DATA_DTYPE,
            header=0)
        return df

    def load_all(self):
        """load all varieties from csv file."""
        dfs = {}
        for variety, file_path in self.varieties_path.items():
            df = self.load_one(file_path)
            dfs[variety] = df
        return dfs

    @staticmethod
    def get_date_set(dfs):
        """get date set from all the contracts."""
        date_set = set()

        for df in dfs.values():
            for date in df.index:
                date_set.add(date)

        return date_set

    def align_one(self, df, date_set):
        """align one variety."""

        paddle_row = copy.deepcopy(df.iloc[0])
        paddle_date = df.index[0]
        for date in date_set:
            if date not in df.index and date < paddle_date:
                df.loc[date] = paddle_row
                df.at[date, types.VALID] = 0

        df.sort_index(inplace=True)

        return df

    def align_all(self):
        """align the datetime"""
        dfs = self.load_all()
        date_set = self.get_date_set(dfs)
        for variety, df in dfs.items():
            new_df = self.align_one(df, date_set)
            file_path = os.path.join(self.dst_dir, f"{variety}.csv")
            new_df.to_csv(file_path, date_format=types.DATE_FORMAT)
