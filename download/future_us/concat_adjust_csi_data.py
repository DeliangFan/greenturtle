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

This script should be used for the CSI data(https://www.csidata.com/).
"""


import copy
import datetime
import os
import re

import pandas as pd

import greenturtle.constants as const
import greenturtle.constants.future as future_const
import greenturtle.data.backtrader.future as future_data
from greenturtle import exception
from greenturtle.util.logging import logging


logger = logging.get_logger()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_DIR = os.path.join(BASE_DIR, "output/source")
ADJUST_DIR = os.path.join(BASE_DIR, "output/adjust")

# pylint: disable=R0801
CSI_DATA_COLUMNS = (
    "datetime",
    future_const.CONTRACT,
    future_const.EXPIRE,
    const.OPEN,
    const.HIGH,
    const.LOW,
    const.CLOSE,
    future_const.VOLUME,
    future_const.OPEN_INTEREST,
    future_const.TOTAL_VOLUME,
    future_const.TOTAL_OPEN_INTEREST,
)

# pylint: disable=R0801
CSI_DATA_DTYPE = {
    "datetime": str,
    future_const.CONTRACT: str,
    future_const.EXPIRE: str,
    const.OPEN: float,
    const.HIGH: float,
    const.LOW: float,
    const.CLOSE: float,
    future_const.VOLUME: int,
    future_const.OPEN_INTEREST: int,
    future_const.TOTAL_VOLUME: int,
    future_const.TOTAL_OPEN_INTEREST: int,
}


class Process2AdjustPrice:

    """
    Process2AdjustPrice generate a csv file with adjusted price

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

    @staticmethod
    def load_dataframe_from_csv_file(file_path):
        """load dataframe from a single csv file."""

        df = pd.read_csv(
            file_path,
            index_col="datetime",
            names=CSI_DATA_COLUMNS,
            dtype=CSI_DATA_DTYPE)

        # convert the datetime from string type to datetime type.
        df.index = df.index.map(
            lambda x: datetime.datetime.strptime(x, "%Y%m%d"))

        df.expire = df.expire.map(
            lambda x: datetime.datetime.strptime(x, "%Y%m%d"))

        # sort and drop the duplicated index row.
        df.sort_index(inplace=True)
        df = df.reset_index().drop_duplicates(
            subset="datetime",
            keep="first").set_index("datetime")

        return df

    def load_dataframes_from_csv_files(self):
        """load dataframes from csv files"""

        # csi data file name pattern format
        pattern = r"^" + self.name + r"_20[0-9][0-9][FGHJKMNQUVXZ]\.csv$"

        files = os.listdir(self.src_dir)
        for file in files:
            # skip file with unexpected name.
            if not re.match(pattern, file):
                continue

            # load single data frame from csv file.
            file_path = os.path.join(self.src_dir, file)
            df = self.load_dataframe_from_csv_file(file_path)

            # add the contract name column.
            contract = file.split(".")[0]
            df[future_const.CONTRACT] = contract
            self.dfs_dict[contract] = df

    def init_adjust_dataframe(self, fromdate=None, todate=None):
        """init the adjusted dataframe with index."""
        date_sets = set()

        # get the valid dates
        for _, df in self.dfs_dict.items():
            for date in df.index:
                # filter the dates out of fromdate and todate
                if fromdate <= date <= todate and date not in date_sets:
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

            row = df.loc[date]
            # set the contract name according to the largest open interest
            if row.open_interest >= largest:
                largest = row.open_interest
                largest_contract = contract

        return largest_contract

    def add_contract_column(self, adjust_df):
        """add contract name column to adjust dataframe."""

        # 1. deepcopy the datetime index and sort descend.
        dates = copy.deepcopy(adjust_df.index)
        sorted_dates = sorted(dates, reverse=True)

        # 2. for every date, choose the contract with the largest amount of
        # open interest as main contract name for adjust dataframe.
        for date in sorted_dates:
            contract = self.get_contract_by_open_interest(date)
            # if contract name not found, raise exception
            if contract is None:
                raise exception.ContractNotFound(contract)
            adjust_df.loc[date, future_const.CONTRACT] = contract

        # 3. do a backward check to make sure the contract name is always
        # continuous by time order.
        newer_contract = adjust_df.iloc[-1][future_const.CONTRACT]

        for date in sorted_dates:
            row = adjust_df.loc[date]
            contract = row[future_const.CONTRACT]

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
                adjust_df.loc[date, future_const.CONTRACT] = \
                    newer_contract

        return adjust_df

    def add_prices_column(self, adjusted_df):
        """add source prices column to adjust dataframe."""
        for date in adjusted_df.index:
            contract = adjusted_df.loc[date, future_const.CONTRACT]
            source_df = self.dfs_dict[contract]

            # prices columns
            adjusted_df.loc[date, const.ORI_OPEN] = \
                source_df.loc[date, const.OPEN]
            adjusted_df.loc[date, const.ORI_HIGH] = \
                source_df.loc[date, const.HIGH]
            adjusted_df.loc[date, const.ORI_LOW] = \
                source_df.loc[date, const.LOW]
            adjusted_df.loc[date, const.ORI_CLOSE] = \
                source_df.loc[date, const.CLOSE]

            # volume
            volume = int(source_df.loc[date, future_const.VOLUME])
            adjusted_df.loc[date, future_const.VOLUME] = volume

            # open interest
            open_interest = \
                int(source_df.loc[date, future_const.OPEN_INTEREST])
            adjusted_df.loc[date, future_const.OPEN_INTEREST] = open_interest

        return adjusted_df

    def add_adjust_factor_column(self, adjusted_df):
        """add adjust factor column to adjust dataframe."""

        # 1. deepcopy the datetime index and sort descend.
        dates = copy.deepcopy(adjusted_df.index)
        sorted_dates = sorted(dates, reverse=True)

        # 2. initiate the factor and newer close price
        newer_contact = adjusted_df.iloc[-1][future_const.CONTRACT]
        factor = 1.0

        # 3. backward compute the factors
        for date in sorted_dates:
            contract = adjusted_df.loc[date, future_const.CONTRACT]
            # multiply the factors when meeting a switch of the contract
            if contract != newer_contact:
                newer_df = self.dfs_dict[newer_contact]
                newer_close_price = newer_df.loc[date, const.CLOSE]
                close_price = adjusted_df.loc[date, const.ORI_CLOSE]
                # compute the factor
                factor = factor * newer_close_price / close_price
                msg = f"compute factor at {date} as contract rolling."
                logger.info(msg)

            newer_contact = contract
            adjusted_df.loc[date, "factor"] = factor

        return adjusted_df

    @staticmethod
    def add_adjust_prices_column(adjusted_df):
        """add adjusted prices column to adjust dataframe."""
        for date in adjusted_df.index:
            factor = adjusted_df.loc[date, "factor"]
            # adjust open
            adjusted_df.loc[date, const.OPEN] = \
                round(factor * adjusted_df.loc[date, const.ORI_OPEN], 6)
            # adjust high
            adjusted_df.loc[date, const.HIGH] = \
                round(factor * adjusted_df.loc[date, const.ORI_HIGH], 6)
            # adjust low
            adjusted_df.loc[date, const.LOW] = \
                round(factor * adjusted_df.loc[date, const.ORI_LOW], 6)
            # adjust close
            adjusted_df.loc[date, const.CLOSE] = \
                round(factor * adjusted_df.loc[date, const.ORI_CLOSE], 6)

        return adjusted_df

    def add_others_column(self, adjusted_df):
        """add others column like volumne to adjust dataframe."""
        for date in adjusted_df.index:
            contract = adjusted_df.loc[date, future_const.CONTRACT]
            source_df = self.dfs_dict[contract]

            # add volume, open interest columns etc
            adjusted_df.loc[date, future_const.EXPIRE] = \
                source_df.loc[date, future_const.EXPIRE]
            adjusted_df.loc[date, future_const.VOLUME] = \
                source_df.loc[date, future_const.VOLUME]
            adjusted_df.loc[date, future_const.TOTAL_VOLUME] = \
                source_df.loc[date, future_const.TOTAL_VOLUME]
            adjusted_df.loc[date, future_const.OPEN_INTEREST] = \
                source_df.loc[date, future_const.OPEN_INTEREST]
            adjusted_df.loc[date, future_const.TOTAL_OPEN_INTEREST] = \
                source_df.loc[date, future_const.TOTAL_OPEN_INTEREST]

        return adjusted_df

    @staticmethod
    def compare_contract_order(older, newer):
        """
        compare contract order according to the string.

        the parameter is string type with {year}_{month_code} format.
        both the year and month are increasing since 2000.

        return true if older <= newer and false otherwise.
        """
        return older <= newer

    def process(self):
        """
        process compute adjust price from many csv files and write to a
        single file.
        """

        self.load_dataframes_from_csv_files()

        adjust_df = self.init_adjust_dataframe(
            fromdate=self.fromdate,
            todate=self.todate)

        adjust_df = self.add_contract_column(adjust_df)
        adjust_df = self.add_prices_column(adjust_df)
        adjust_df = self.add_adjust_factor_column(adjust_df)
        adjust_df = self.add_adjust_prices_column(adjust_df)
        adjust_df = self.add_others_column(adjust_df)

        # set the order for columns
        adjust_df = adjust_df[future_data.COLUMN_ORDER]

        if not os.path.exists(self.dst_dir):
            os.makedirs(self.dst_dir)

        dst_path = os.path.join(self.dst_dir, f"{self.name}.csv")
        adjust_df.to_csv(dst_path)


if __name__ == "__main__":

    for group in future_const.FUTURE.values():
        for future_name, future in group.items():
            src_directory = os.path.join(SOURCE_DIR, future_name)
            if not os.path.exists(src_directory):
                continue

            # initiate the process
            p = Process2AdjustPrice(
                future_name,
                fromdate=datetime.datetime(2005, 2, 1),
                todate=datetime.datetime(2025, 2, 6),
                src_dir=src_directory,
                dst_dir=ADJUST_DIR)

            p.process()
