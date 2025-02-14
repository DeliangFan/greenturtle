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

"""
Script to generate continuous dataframe from many contract file with
adjusted prices.
"""


import abc
import copy
import datetime
import os
import re

import pandas as pd

from greenturtle.constants.future import types
from greenturtle.data import validation
from greenturtle import exception
from greenturtle.util.logging import logging


logger = logging.get_logger()


class GenerateContinuous:

    """
    GenerateContinuous generate a csv file with adjusted price

    1. load the dataframe for individual contract csv file
    2. choose select the main contract according to the open interest
       for a specific date.
    3. combine main contract dataframes to a continuous dataframe
    4. adjust the open/high/low/close price with backward approach
    5. write to a single csv file.
    """

    # pylint: disable=too-many-positional-arguments,too-many-arguments
    def __init__(self,
                 name,
                 fromdate=None,
                 todate=None,
                 src_dir=None,
                 dst_dir=None):

        self.name = name
        self.fromdate = fromdate
        self.todate = todate
        self.src_dir = src_dir
        self.dst_dir = dst_dir
        self.dfs_dict = {}

    def load_one(self, file_path):
        """load dataframe from a single csv file."""

        names = [types.DATETIME] + types.CONTRACT_COLUMN
        df = pd.read_csv(
            file_path,
            index_col=types.DATETIME,
            names=names,
            dtype=types.CONTRACT_DATA_DTYPE)

        # convert the datetime from string type to datetime type.
        df.index = df.index.map(
            lambda x: datetime.datetime.strptime(x, "%Y%m%d"))

        df.expire = df.expire.map(
            lambda x: datetime.datetime.strptime(x, "%Y%m%d"))

        # sort and drop the duplicated index row.
        df.sort_index(inplace=True)
        df = df.reset_index().drop_duplicates(
            subset=types.DATETIME,
            keep="first").set_index(types.DATETIME)

        self._validate_and_fix(df, file_path)

        return df

    @staticmethod
    def _validate_and_fix(df, file_path):
        """validate the data and fix abnormal data."""
        contracts = set()
        for index, row in df.iterrows():
            try:
                # 1. validate the price
                validation.validate_price(
                    row[types.OPEN],
                    row[types.HIGH],
                    row[types.LOW],
                    row[types.CLOSE],
                )
                # 2. prepare validating for contracts
                contracts.add(row[types.CONTRACT])
            except (
                    exception.DataLowPriceAbnormalError,
                    exception.DataHighPriceAbnormalError):

                msg = f"validate {file_path} at {index} failed, try to fix"
                logger.warning(msg)

                df.at[index, types.LOW] = min(
                    row[types.OPEN],
                    row[types.HIGH],
                    row[types.LOW],
                    row[types.CLOSE],
                )

                df.at[index, types.HIGH] = max(
                    row[types.OPEN],
                    row[types.HIGH],
                    row[types.LOW],
                    row[types.CLOSE],
                )

        # validate the contract
        if len(contracts) != 1:
            raise exception.DataContractAbnormalError()

    @abc.abstractmethod
    def get_pattern(self):
        """get the pattern for file name"""
        raise NotImplementedError

    def load_all(self):
        """load dataframes from csv files"""

        pattern = self.get_pattern()
        for file in os.listdir(self.src_dir):
            # skip file with unexpected name.
            if not re.match(pattern, file):
                continue

            # load single data frame from csv file.
            file_path = os.path.join(self.src_dir, file)
            df = self.load_one(file_path)

            if len(df) > 0:
                contract = df.iloc[0][types.CONTRACT]
                self.dfs_dict[contract] = df

    def init_output_df(self):
        """init the new dataframe with index."""
        date_sets = set()

        # get the valid dates
        for _, df in self.dfs_dict.items():
            for date in df.index:
                # filter the dates out of fromdate and todate
                if (
                        (self.fromdate <= date <= self.todate) and
                        (date not in date_sets)
                ):
                    date_sets.add(date)

        # init and sort dataframe with datetime index
        df = pd.DataFrame(index=list(date_sets))
        df.sort_index(inplace=True)

        return df

    def get_contract_by_open_interest(self, date):
        """get contract name according to the largest open interest"""

        largest = 0
        largest_contract = None
        for contract, df in self.dfs_dict.items():
            # skip unwanted date
            if date not in df.index:
                continue

            # set the contract name according to the largest open interest
            open_interest = df.loc[date][types.OPEN_INTEREST]
            if open_interest >= largest:
                largest = open_interest
                largest_contract = contract

        return largest_contract

    def add_contract_column(self, df):
        """add contract name column to adjust dataframe."""

        # 1. deepcopy the datetime index and sort descend.
        dates = copy.deepcopy(df.index)
        sorted_dates = sorted(dates, reverse=True)

        # 2. for every date, choose the contract with the largest amount of
        # open interest as main contract name for adjust dataframe.
        for date in sorted_dates:
            contract = self.get_contract_by_open_interest(date)
            # if contract name not found, raise exception
            if contract is None:
                raise exception.ContractNotFound(contract)
            df.at[date, types.CONTRACT] = contract

        # 3. do a backward check to make sure the contract name is always
        # continuous by time order.
        newer_contract = df.iloc[-1][types.CONTRACT]
        for date in sorted_dates:
            row = df.loc[date]
            contract = row[types.CONTRACT]

            if self.compare_contract_order(
                    older=contract,
                    newer=newer_contract):
                newer_contract = contract
            else:
                msg = f"a newer contract {contract} for " + \
                      f"future {self.name} at date {date} occurs, " + \
                      f"which should not newer than {newer_contract}"
                logger.warning(msg)
                # correct the abnormal contract name.
                df.at[date, types.CONTRACT] = newer_contract

        return df

    def add_prices_column(self, df):
        """add source prices column to adjust dataframe."""

        for date in df.index:
            contract = df.loc[date, types.CONTRACT]
            contract_df = self.dfs_dict[contract]

            # prices columns
            df.loc[date, types.ORI_OPEN] = contract_df.loc[date, types.OPEN]
            df.loc[date, types.ORI_HIGH] = contract_df.loc[date, types.HIGH]
            df.loc[date, types.ORI_LOW] = contract_df.loc[date, types.LOW]
            df.loc[date, types.ORI_CLOSE] = contract_df.loc[date, types.CLOSE]

        return df

    def add_adjust_factor_column(self, df):
        """add adjust factor column to adjust dataframe."""

        # 1. deepcopy the datetime index and sort descend.
        dates = copy.deepcopy(df.index)
        sorted_dates = sorted(dates, reverse=True)

        # 2. initiate the factor and newer close price
        newer_contract = df.iloc[-1][types.CONTRACT]
        adjust_factor = 1.0

        # 3. backward compute the factors
        for date in sorted_dates:
            contract = df.loc[date, types.CONTRACT]
            if contract != newer_contract:
                newer_contract_df = self.dfs_dict[newer_contract]

                # get the price
                newer_close_price = newer_contract_df.loc[date, types.CLOSE]
                close_price = df.loc[date, types.ORI_CLOSE]

                # multiply the factors when meeting a switch of the contract
                adjust_factor *= newer_close_price / close_price
                msg = f"compute factor at {date} as contract rolling."
                logger.info(msg)

            # 4. set the adjust factor
            newer_contract = contract
            df.loc[date, types.ADJUST_FACTOR] = adjust_factor

        return df

    @staticmethod
    def add_adjust_prices_column(df):
        """
        add adjusted prices column to adjust dataframe according to the
        adjust factor.
        """

        for date in df.index:
            adjust_factor = df.loc[date, types.ADJUST_FACTOR]
            # adjust open
            df.loc[date, types.OPEN] = \
                round(adjust_factor * df.loc[date, types.ORI_OPEN], 6)
            # adjust high
            df.loc[date, types.HIGH] = \
                round(adjust_factor * df.loc[date, types.ORI_HIGH], 6)
            # adjust low
            df.loc[date, types.LOW] = \
                round(adjust_factor * df.loc[date, types.ORI_LOW], 6)
            # adjust close
            df.loc[date, types.CLOSE] = \
                round(adjust_factor * df.loc[date, types.ORI_CLOSE], 6)

        return df

    def add_others_column(self, df):
        """add others column like volumne to adjust dataframe."""
        for date in df.index:
            contract = df.loc[date, types.CONTRACT]
            contract_df = self.dfs_dict[contract]

            # add volume, open interest columns etc
            df.loc[date, types.EXPIRE] = contract_df.loc[date, types.EXPIRE]
            df.loc[date, types.VOLUME] = contract_df.loc[date, types.VOLUME]
            df.loc[date, types.TOTAL_VOLUME] = \
                contract_df.loc[date, types.TOTAL_VOLUME]
            df.loc[date, types.OPEN_INTEREST] = \
                contract_df.loc[date, types.OPEN_INTEREST]
            df.loc[date, types.TOTAL_OPEN_INTEREST] = \
                contract_df.loc[date, types.TOTAL_OPEN_INTEREST]

        return df

    @staticmethod
    def compare_contract_order(older, newer):
        """
        compare contract order according to the string.

        the parameter is string type with {year}_{month_code} format.
        both the year and month are increasing since 2000.

        return true if older <= newer and false otherwise.
        """
        return older <= newer

    def generate(self):
        """
        generate adjust price from many csv files and write to a
        single file.
        """

        self.load_all()

        df = self.init_output_df()
        df = self.add_contract_column(df)
        df = self.add_prices_column(df)
        df = self.add_adjust_factor_column(df)
        df = self.add_adjust_prices_column(df)
        df = self.add_others_column(df)

        # set the order for columns
        df = df[types.CONTINUOUS_COLUMN]

        if not os.path.exists(self.dst_dir):
            os.makedirs(self.dst_dir)

        dst_path = os.path.join(self.dst_dir, f"{self.name}.csv")
        df.to_csv(dst_path)


class GenerateContinuousFromCSIData(GenerateContinuous):
    """
    GenerateContinuousFromCSIData generate a csv file with adjusted price
    from csi data.
    """

    def get_pattern(self):
        """csi data file name pattern format"""
        pattern = r"^" + self.name + r"_20[0-9][0-9][FGHJKMNQUVXZ]\.csv$"
        if self.name in ("BTC", "ETH"):
            pattern = r"^" + self.name + r"20[0-9][0-9][FGHJKMNQUVXZ]\.csv$"

        return pattern
