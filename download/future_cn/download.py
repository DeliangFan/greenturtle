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

"""Download the cn future data from exchanges.

交易所               交易所代码	合约后缀     地址
中国金融期货交易所	    CFFEX	    .CFX	    http://www.cffex.com.cn
上海期货交易所	    SHFE	    .SHF	    https://www.shfe.com.cn
上海国际能源交易中心	INE	        .INE	    https://www.ine.cn
郑州商品交易所	    CZCE	    .ZCE	    http://www.czce.com.cn
大连商品交易所	    DCE	        .DCE	    http://www.dce.com.cn
广州期货交易所	    GFEX	    .GFEX	    http://www.gfex.com.cn
"""

import calendar
import datetime
import os

import akshare as ak
import pandas as pd

import greenturtle.constants.future as future_const
import greenturtle.constants as const
from greenturtle import exception
from greenturtle.util.logging import logging


logger = logging.get_logger()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

MARKETS_CN = {
    "CFFEX": {
        "start_year": 2010,
        "end_year": 2024,
    },
    "DCE": {
        "start_year": 2001,
        "end_year": 2024,
    },
    "SHFE": {
        "start_year": 1992,
        "end_year": 2024,
    },
    "INE": {
        "start_year": 1990,
        "end_year": 2024,
    },
    "CZCE": {
        "start_year": 1990,
        "end_year": 2024,
    },
    "GFEX": {
        "start_year": 1990,
        "end_year": 2024,
    },
}

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


class FutureCNDownload:
    """
    FutureCNDownload used for downloading the cn future data from
    exchanges.
    """

    def __init__(self):
        pass

    def get_months(self, start_year, end_year):
        """get the month list with start date and end date."""
        months = []

        for year in range(start_year, end_year):
            for month in range(1, 13):
                # use calendar.mongthrange to get month last day
                monthrange = calendar.monthrange(year, month)
                start_day = f"{year}{month:02d}01"
                end_day = f"{year}{month:02d}{monthrange[1]:02d}"
                months.append((start_day, end_day))

        return months

    def download_month_data_by_market(self, start_date, end_date, market):
        """
        Do download the month data by market

        please refer the following link for more details
        https://akshare.akfamily.xyz/data/futures/futures.html#id53
        """
        retry = 5

        while retry > 0:
            try:
                df = ak.get_futures_daily(
                    start_date=start_date,
                    end_date=end_date,
                    market=market)
                # return the result if success
                return df

            # pylint: disable=broad-except
            except Exception:
                retry -= 1
                msg = f"failed download {market} {start_date}-{end_date}"
                logger.warning(msg)

        # raise exception after 5 times retry
        raise exception.DownloadDataError

    def download_data_by_market(self, market):
        """download the data by market"""

        # make market directory if not exists.
        dst_dir = os.path.join(OUTPUT_DIR, market)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)

        start_year = MARKETS_CN[market]["start_year"]
        end_year = MARKETS_CN[market]["end_year"]
        months = self.get_months(start_year, end_year)

        # download the month data
        for start_date, end_date in months:
            file_path = os.path.join(dst_dir, f"{start_date}-{end_date}.csv")

            # skip download if the file already exists
            # the download progress take a very long time.
            if os.path.exists(file_path):
                continue

            # download the file
            msg = f"try to download {market} {start_date}-{end_date}"
            logger.info(msg)

            df = self.download_month_data_by_market(
                start_date,
                end_date,
                market)

            if len(df) > 0:
                # write to the file if it's not a empty data
                df.to_csv(file_path)

                msg = f"download {market} {start_date}-{end_date} success"
                logger.info(msg)
            else:
                msg = f"empty data for {market} {start_date}-{end_date}"
                logger.info(msg)

    def download_all_markets_data(self):
        """download all the data

        1. download the data to output/{market}/{data}.csv
        2. generate the contract data to output/source/{future}/{contract}.csv
        3. generate the adjust data to output/adjust/{future}.csv
        """
        for market in MARKETS_CN:
            logger.info("start to download market %s", market)
            self.download_data_by_market(market)
            logger.info("market %s download finished", market)
            # TODO(fixme)
            self.generate_contract_csvs_by_market(market)

    def load_dataframe_from_csv_file(self, file_path):
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

        # TODO(fix me)
        # get the expire date by contract
        # df.expire = df.expire.map(
        #    lambda x: datetime.datetime.strptime(x, "%Y%m%d"))

        # sort and drop the duplicated index row.
        df.sort_index(inplace=True)
        # df = df.reset_index().drop_duplicates(
        #    subset=const.DATETIME,
        #    keep="first").set_index("datetime")

        # TODO(fix me)
        # self._validate_and_fix(df, file_path)

        return df

    def load_dataframe_by_market(self, market):
        """load dataframe from all the csv file by market."""

        df_list = []

        src_dir = os.path.join(OUTPUT_DIR, market)
        for file in os.listdir(src_dir):
            file_path = os.path.join(src_dir, file)
            # load the dataframe for single csv file.
            df = self.load_dataframe_from_csv_file(file_path)
            df_list.append(df)

        return pd.concat(df_list)

    def list_futures(self, df):
        """list all the future from the concat dataframe"""
        futures = set()

        for _, row in df.iterrows():
            future = row[future_const.VARIETY]
            futures.add(future)

        return futures

    def list_contracts(self, df, future):
        """list all the contract from the concat dataframe"""
        contracts = set()

        for _, row in df.iterrows():
            variety = row[future_const.VARIETY]
            if future != variety:
                continue

            contract = row[future_const.CONTRACT]
            contracts.add(contract)

        return contracts

    def generate_single_contract_csv(self, df, future, contract, dst_dir):
        """generate single contract csv file."""

        # create a dedicated future directory
        future_dst_dir = os.path.join(dst_dir, future)
        if not os.path.exists(future_dst_dir):
            os.makedirs(future_dst_dir)

        file_path = os.path.join(future_dst_dir, f"{contract}.csv")
        contract_df = df[df[future_const.CONTRACT] == contract]
        contract_df.to_csv(file_path)

    def generate_contract_csvs_by_market(self, market):
        """generate contract files"""

        # create the source directory if not exists
        dst_dir = os.path.join(OUTPUT_DIR, "source")

        # 1. get all of the data by markert
        df = self.load_dataframe_by_market(market)

        # 2. list all of the future
        futures = self.list_futures(df)
        for future in futures:

            # 3. list all of the contract by future
            contracts = self.list_contracts(df, future)
            for contract in contracts:

                # 4. generate single contract csv file
                self.generate_single_contract_csv(
                    df,
                    future,
                    contract,
                    dst_dir)


if __name__ == '__main__':

    d = FutureCNDownload()
    d.download_all_markets_data()
