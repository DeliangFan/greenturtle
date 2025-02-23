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

"""Generate future contract files from original data."""

import abc
import datetime
import os

import numpy as np
import pandas as pd

from greenturtle.constants.future import types
from greenturtle.util.logging import logging


logger = logging.get_logger()


# pylint: disable=R0801
AKSHARE_DATA_COLUMNS = (
    types.ID,
    types.CONTRACT,
    types.DATETIME,
    types.OPEN,
    types.HIGH,
    types.LOW,
    types.CLOSE,
    types.VOLUME,
    types.OPEN_INTEREST,
    types.TURN_OVER,
    types.SETTLE,
    types.PRE_SETTLE,
    types.VARIETY,
)

# pylint: disable=R0801
AKSHARE_DATA_DTYPE = {
    types.ID: int,
    types.CONTRACT: str,
    types.DATETIME: str,
    types.OPEN: float,
    types.HIGH: float,
    types.LOW: float,
    types.CLOSE: float,
    types.VOLUME: "Int64",
    types.OPEN_INTEREST: float,
    types.TURN_OVER: float,
    types.SETTLE: float,
    types.PRE_SETTLE: float,
    types.VARIETY: str,
}


# pylint: disable=too-few-public-methods
class GenerateContract:
    """
    GenerateContract generate the single future contract csv file.

    It read data from the source directory and write the single future
    to the destination directory, which looks like.
    dst_dir
      /{future}
        /{contract1}.csv
        /{contract2}.csv
      /{future}
        /{contract3}.csv
        ...
    """

    def __init__(self, markets, src_dir, dst_dir):
        self.markets = markets
        self.src_dir = src_dir
        self.dst_dir = dst_dir

    @abc.abstractmethod
    def generate(self):
        """generate the contract csv file."""
        raise NotImplementedError


class GenerateContractFromAKShare(GenerateContract):
    """
    Generate contract file from the data downloaded by akshare.
    """

    def generate(self):
        """generate the contract csv file."""
        for market in self.markets:
            self.generate_by_market(market)

    def generate_by_market(self, market):
        """generate the contract csv file by market."""
        # 1. get all the data by market
        df = self.load_all_by_market(market)

        # 2. list all the futures
        varietis = self.list_varietis(df)
        for variety in varietis:
            # 3. list all the contracts by future
            contracts = self.list_contracts(df, variety)
            for contract in contracts:
                # 4. generate single contract csv file
                self.generate_one(df, variety, contract)

    @staticmethod
    def load_one(file_path):
        """load dataframe from a single csv file."""

        df = pd.read_csv(
            file_path,
            index_col=types.DATETIME,
            names=AKSHARE_DATA_COLUMNS,
            dtype=AKSHARE_DATA_DTYPE,
            header=0)

        # convert the datetime from string type to datetime type.
        df.index = df.index.map(
            lambda x: datetime.datetime.strptime(x, types.DATE_FORMAT))

        # sort and drop the duplicated index row.
        df.sort_index(inplace=True)

        return df

    def load_all_by_market(self, market):
        """load source data from all the csv file by market."""

        df_list = []
        dir_path = str(os.path.join(self.src_dir, market))
        for file in os.listdir(dir_path):
            file_path = os.path.join(dir_path, file)
            # load the dataframe for single csv file.
            df = self.load_one(file_path)
            df_list.append(df)

        return pd.concat(df_list)

    @staticmethod
    def list_varietis(df):
        """list all the varieties from the concat dataframe"""
        varieties = set()

        for _, row in df.iterrows():
            variety = row[types.VARIETY]
            varieties.add(variety)

        return varieties

    @staticmethod
    def list_contracts(df, variety):
        """list all the contract from the concat dataframe"""
        contracts = set()

        for _, row in df.iterrows():
            if variety != row[types.VARIETY]:
                continue

            contract = row[types.CONTRACT]
            contracts.add(contract)

        return contracts

    def generate_one(self, df, variety, contract):
        """generate single contract csv file."""

        # 1. create a dedicated future directory
        variety_dst_dir = str(os.path.join(self.dst_dir, variety))
        if not os.path.exists(variety_dst_dir):
            os.makedirs(variety_dst_dir)

        # 2. filter the data by contract
        contract_df = df[df[types.CONTRACT] == contract].copy()

        # 3. sort by index and remove duplicates
        contract_df.sort_index(inplace=True)
        contract_df = contract_df.reset_index().drop_duplicates(
            subset=types.DATETIME,
            keep="first").set_index(types.DATETIME)

        # 4. add other columns
        for index, row in contract_df.iterrows():
            future = row[types.VARIETY]
            # get total volume
            total_volume = self.get_total_volume(df, index, future)
            contract_df.loc[index, types.TOTAL_VOLUME] = total_volume
            # get total open interest
            total_open_interest = \
                self.get_total_open_interest(df, index, future)
            contract_df.loc[index, types.TOTAL_OPEN_INTEREST] = \
                total_open_interest

        # TODO(fixme) get the expire date by contract
        contract_df[types.EXPIRE] = np.nan
        # 5. filter unwanted column and sort the order of columns
        contract_df = contract_df[types.CONTRACT_COLUMN]

        # 6. write to csv file
        file_path = os.path.join(variety_dst_dir, f"{contract}.csv")
        contract_df.to_csv(
            file_path,
            header=False,
            date_format=types.DATE_FORMAT)

    @staticmethod
    def get_total_volume(df, index, variety):
        """get total volumes for a future by date"""

        total_volume = 0

        # filter by index(date) and future
        df = df[df.index.isin([index])]
        df = df[df[types.VARIETY] == variety]

        for _, row in df.iterrows():
            volume = row[types.VOLUME]
            total_volume += volume

        return total_volume

    @staticmethod
    def get_total_open_interest(df, index, variety):
        """get total open interest for a future by date"""

        total_open_interest = 0

        # filter by index(date) and future
        df = df[df.index.isin([index])]
        df = df[df[types.VARIETY] == variety]

        for _, row in df.iterrows():
            open_interest = row[types.OPEN_INTEREST]
            total_open_interest += open_interest

        return total_open_interest
