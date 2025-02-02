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

"""script to generate continuous dataframe from many contract file."""


import copy
import datetime
import os

import pandas as pd

import greenturtle.constants.future as future_const
from greenturtle import exception
from greenturtle.util.logging import logging


logger = logging.get_logger()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_DIR = os.path.join(BASE_DIR, "output/source")
ADJUST_DIR = os.path.join(BASE_DIR, "output/adjust")
# pylint: disable=R0801
COLUMNS = (
    "id",
    "datetime",
    "open",
    "high",
    "low",
    "close",
    "volume",
    "open_interest",
)
# pylint: disable=R0801
DTYPE = {
    "open": float,
    "high": float,
    "low": float,
    "close": float,
    "volume": float,
    "open_interest": float,
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
                 category,
                 fromdate=None,
                 todate=None,
                 src_dir=None,
                 dst_dir=None):

        self.name = name
        self.category = category
        self.fromdate = fromdate
        self.todate = todate
        self.src_dir = src_dir
        self.dst_dir = dst_dir
        self.dfs_dict = {}

    # TODO(wsfdl)
    @staticmethod
    def load_dataframe_from_csv_file(file_path):
        """load dataframe from a single csv file."""

        df = pd.read_csv(
            file_path,
            index_col="datetime",
            names=COLUMNS,
            dtype=DTYPE,
            header=0)

        # remove some abnormal data since it always occur in the
        # first or last line.
        df = df.iloc[1:-1]

        # remove unwanted id column
        df.drop("id", axis=1, inplace=True)

        # convert the datetime from string type to datetime type.
        df.index = df.index.map(
            lambda x: datetime.datetime.strptime(x, "%Y-%m-%d"))

        # sort and drop the duplicated index row.
        df.sort_index(inplace=True)
        df = df.reset_index().drop_duplicates(
            subset="datetime",
            keep="first").set_index("datetime")

        return df

    def load_dataframes_from_csv_files(self):
        """load dataframes from csv files"""

        files = os.listdir(self.src_dir)
        for file in files:
            # skip non csv data file.
            if not file.endswith(".csv"):
                continue

            # load single data frame from csv file.
            file_path = os.path.join(self.src_dir, file)
            df = self.load_dataframe_from_csv_file(file_path)

            # add the contract name column.
            contract_name = file.split(".")[0]
            df[future_const.CONTRACT_NAME] = contract_name
            self.dfs_dict[contract_name] = df

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

    def get_contract_name_by_open_interest(self, date):
        """get contract name according to the largest open interest"""

        largest = 0
        largest_contract_name = None

        for contract_name, df in self.dfs_dict.items():
            # skip unwanted date
            if date not in df.index:
                continue

            row = df.loc[date]
            # set the contract name according to the largest open interest
            if row.open_interest > largest:
                largest = row.open_interest
                largest_contract_name = contract_name

        return largest_contract_name

    def add_contract_name_column(self, adjust_df):
        """add contract name column to adjust dataframe."""

        # 1. deepcopy the datetime index and sort descend.
        dates = copy.deepcopy(adjust_df.index)
        sorted_dates = sorted(dates, reverse=True)

        # 2. for every date, choose the contract with the largest amount of
        # open interest as main contract name for adjust dataframe.
        for date in sorted_dates:
            contract_name = self.get_contract_name_by_open_interest(date)
            # if contract name not found, raise exception
            if contract_name is None:
                raise exception.ContractNameNotFound(contract_name)
            adjust_df.loc[date, future_const.CONTRACT_NAME] = contract_name

        # 3. do a backward check to make sure the contract name is always
        # continuous by time order.
        newer_contract_name = adjust_df.iloc[-1][future_const.CONTRACT_NAME]

        for date in sorted_dates:
            row = adjust_df.loc[date]
            contract_name = row[future_const.CONTRACT_NAME]

            if self.compare_contract_name_order(
                    older=contract_name,
                    newer=newer_contract_name):
                newer_contract_name = contract_name
            else:
                msg = f"a newer contract {contract_name} for " + \
                      f"future {self.name} at date {date} occurs, " + \
                      f"which should not newer than {newer_contract_name}"
                logger.warning(msg)
                # correct the abnormal contract name.
                adjust_df.loc[date, future_const.CONTRACT_NAME] = \
                    newer_contract_name

        return adjust_df

    def add_prices_column(self, adjusted_df):
        """add source prices column to adjust dataframe."""
        for date in adjusted_df.index:
            contract_name = adjusted_df.loc[date, "contract_name"]
            source_df = self.dfs_dict[contract_name]
            # prices columns
            adjusted_df.loc[date, "open"] = source_df.loc[date, "open"]
            adjusted_df.loc[date, "high"] = source_df.loc[date, "high"]
            adjusted_df.loc[date, "low"] = source_df.loc[date, "low"]
            adjusted_df.loc[date, "close"] = source_df.loc[date, "close"]
            # volume
            volume = int(source_df.loc[date, "volume"])
            adjusted_df.loc[date, "volume"] = volume
            # open interest
            open_interest = int(source_df.loc[date, "open_interest"])
            adjusted_df.loc[date, "open_interest"] = open_interest

        return adjusted_df

    def add_adjust_factor_column(self, adjusted_df):
        """add adjust factor column to adjust dataframe."""

        # 1. deepcopy the datetime index and sort descend.
        dates = copy.deepcopy(adjusted_df.index)
        sorted_dates = sorted(dates, reverse=True)

        # 2. initiate the factor and newer close price
        newer_contact_name = adjusted_df.iloc[-1][future_const.CONTRACT_NAME]
        factor = 1.0

        # 3. backward compute the factors
        for date in sorted_dates:
            contract_name = adjusted_df.loc[date, future_const.CONTRACT_NAME]
            # multiply the factors when meeting a switch of the contract
            if contract_name != newer_contact_name:
                newer_df = self.dfs_dict[newer_contact_name]
                newer_close_price = newer_df.loc[date, "close"]
                close_price = adjusted_df.loc[date, "close"]
                # compute the factor
                factor = factor * newer_close_price / close_price
                msg = f"compute factor at {date} as contract rolling."
                logger.info(msg)

            newer_contact_name = contract_name
            adjusted_df.loc[date, "factor"] = factor

        return adjusted_df

    def add_adjust_prices_column(self, adjusted_df):
        """add adjusted prices column to adjust dataframe."""
        for date in adjusted_df.index:
            factor = adjusted_df.loc[date, "factor"]
            # adjust open
            adj_open = round(factor * adjusted_df.loc[date, "open"], 6)
            adjusted_df.loc[date, "adj_open"] = adj_open
            # adjust high
            adj_high = round(factor * adjusted_df.loc[date, "high"], 6)
            adjusted_df.loc[date, "adj_high"] = adj_high
            # adjust low
            adj_low = round(factor * adjusted_df.loc[date, "low"], 6)
            adjusted_df.loc[date, "adj_low"] = adj_low
            # adjust close
            adj_close = round(factor * adjusted_df.loc[date, "close"], 6)
            adjusted_df.loc[date, "adj_close"] = adj_close
        return adjusted_df

    def compare_contract_name_order(self, older, newer):
        """
        compare contract name order according to the string.

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
        adjust_df = self.add_contract_name_column(adjust_df)
        adjust_df = self.add_prices_column(adjust_df)
        adjust_df = self.add_adjust_factor_column(adjust_df)
        adjust_df = self.add_adjust_prices_column(adjust_df)

        if self.category in future_const.FUTURE:
            category = future_const.FUTURE[self.category]
            if self.name in category:
                future = category[self.name]
                adjust_df[future_const.CONTRACT_UNIT] = \
                    future[future_const.CONTRACT_UNIT]
                adjust_df[future_const.MARGIN_REQUIREMENT_RATIO] = \
                    future[future_const.MARGIN_REQUIREMENT_RATIO]

        if not os.path.exists(self.dst_dir):
            os.makedirs(self.dst_dir)

        dst_path = os.path.join(self.dst_dir, f"{self.name}.csv")
        adjust_df.to_csv(dst_path)


if __name__ == "__main__":
    NAME = "GC"
    CATEGORY = "metal"
    p = Process2AdjustPrice(
        NAME,
        CATEGORY,
        fromdate=datetime.datetime(2008, 1, 1),
        todate=datetime.datetime(2024, 12, 31),
        src_dir=os.path.join(SOURCE_DIR, NAME),
        dst_dir=ADJUST_DIR)
    p.process()
