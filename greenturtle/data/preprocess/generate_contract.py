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

import greenturtle.constants.future as future_const
import greenturtle.constants as const
from greenturtle.util.logging import logging


logger = logging.get_logger()


# pylint: disable=R0801
AKSHARE_DATA_COLUMNS = (
    const.ID,
    future_const.CONTRACT,
    const.DATETIME,
    const.OPEN,
    const.HIGH,
    const.LOW,
    const.CLOSE,
    future_const.VOLUME,
    future_const.OPEN_INTEREST,
    const.TURN_OVER,
    future_const.SETTLE,
    future_const.PRE_SETTLE,
    future_const.VARIETY,
)

# pylint: disable=R0801
AKSHARE_DATA_DTYPE = {
    const.ID: int,
    future_const.CONTRACT: str,
    const.DATETIME: str,
    const.OPEN: float,
    const.HIGH: float,
    const.LOW: float,
    const.CLOSE: float,
    future_const.VOLUME: int,
    future_const.OPEN_INTEREST: float,
    const.TURN_OVER: float,
    future_const.SETTLE: float,
    future_const.PRE_SETTLE: float,
    future_const.VARIETY: str,
}

CONTRACT_COLUMN = [
    future_const.CONTRACT,
    future_const.EXPIRE,
    const.OPEN,
    const.HIGH,
    const.LOW,
    const.CLOSE,
    future_const.VOLUME,
    future_const.TOTAL_VOLUME,
    future_const.OPEN_INTEREST,
    future_const.TOTAL_OPEN_INTEREST,
]


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

    def __init__(self, markets, src_dir, dst_dir):
        super().__init__(markets, src_dir, dst_dir)

    def generate(self):
        """generate the contract csv file."""
        for market in self.markets:
            self.generate_by_market(market)

    def generate_by_market(self, market):
        """generate the contract csv file by market."""
        # 1. get all the data by market
        df = self.load_all_by_market(market)

        # 2. list all the futures
        futures = self.list_futures(df)
        for future in futures:
            # 3. list all the contracts by future
            contracts = self.list_contracts(df, future)
            for contract in contracts:
                # 4. generate single contract csv file
                self.generate_one(df, future, contract)

    @staticmethod
    def load_one(file_path):
        """load dataframe from a single csv file."""

        df = pd.read_csv(
            file_path,
            index_col=const.DATETIME,
            names=AKSHARE_DATA_COLUMNS,
            dtype=AKSHARE_DATA_DTYPE,
            header=0)

        # convert the datetime from string type to datetime type.
        df.index = df.index.map(
            lambda x: datetime.datetime.strptime(x, "%Y%m%d"))

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
    def list_futures(df):
        """list all the future from the concat dataframe"""
        futures = set()

        for _, row in df.iterrows():
            future = row[future_const.VARIETY]
            futures.add(future)

        return futures

    @staticmethod
    def list_contracts(df, future):
        """list all the contract from the concat dataframe"""
        contracts = set()

        for _, row in df.iterrows():
            variety = row[future_const.VARIETY]
            if future != variety:
                continue

            contract = row[future_const.CONTRACT]
            contracts.add(contract)

        return contracts

    def generate_one(self, df, future, contract):
        """generate single contract csv file."""

        # 1. create a dedicated future directory
        future_dst_dir = str(os.path.join(self.dst_dir, future))
        if not os.path.exists(future_dst_dir):
            os.makedirs(future_dst_dir)

        # 2. filter the data by contract
        contract_df = df[df[future_const.CONTRACT] == contract].copy()

        # 3. sort by index and remove duplicates
        contract_df.sort_index(inplace=True)
        contract_df = contract_df.reset_index().drop_duplicates(
            subset=const.DATETIME,
            keep="first").set_index(const.DATETIME)

        # 4. add other columns
        for index, row in contract_df.iterrows():
            future = row[future_const.VARIETY]
            # get total volume
            total_volume = self.get_total_volume(df, index, future)
            contract_df.loc[index, future_const.TOTAL_VOLUME] = total_volume
            # get total open interest
            total_open_interest = \
                self.get_total_open_interest(df, index, future)
            contract_df.loc[index, future_const.TOTAL_OPEN_INTEREST] = \
                total_open_interest

        # TODO(fixme) get the expire date by contract
        contract_df[future_const.EXPIRE] = np.nan
        # filter unwanted column and sort the order of columns
        contract_df = contract_df[CONTRACT_COLUMN]

        # write to csv file
        file_path = os.path.join(future_dst_dir, f"{contract}.csv")
        contract_df.to_csv(file_path, header=False)

    @staticmethod
    def get_total_volume(df, index, future):
        """get total volumes for a future by date"""

        total_volume = 0

        # filter by index(date) and future
        df = df[df.index.isin([index])]
        df = df[df[future_const.VARIETY] == future]

        for _, row in df.iterrows():
            volume = row[future_const.VOLUME]
            total_volume += volume

        return total_volume

    @staticmethod
    def get_total_open_interest(df, index, future):
        """get total open interesst for a future by date"""

        total_open_interest = 0

        # filter by index(date) and future
        df = df[df.index.isin([index])]
        df = df[df[future_const.VARIETY] == future]

        for _, row in df.iterrows():
            open_interest = row[future_const.OPEN_INTEREST]
            total_open_interest += open_interest

        return total_open_interest
