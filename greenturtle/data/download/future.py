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

"""Download the cn future data from exchanges."""

import abc
import calendar
import datetime
import os
import time

import akshare as ak
import pandas as pd

from greenturtle.constants import types
from greenturtle import exception
from greenturtle.util import calendar as util_calendar
from greenturtle.util.logging import logging


logger = logging.get_logger()


# pylint: disable=too-few-public-methods
class CNFuture:
    """
    FutureCN download used for downloading the cn future data by month.

    It will keep the original data format and write them to csv format
    files in the dst directory.

    The dst directory will look like
    dst_dir
      /{exchange0}
        /{file0}.csv
        /{file1}.csv
      /{exchange1}
        /{file2}.csv
        ...
    """
    def __init__(self, exchanges):
        self.exchanges = exchanges

    @abc.abstractmethod
    def download(self):
        """download all the data."""
        raise NotImplementedError


class CNFutureFromAKShare(CNFuture):
    """
    FutureCNDownload used for downloading the cn future data from
    exchanges by month.
    """

    def download_data_by_period(self, start_date, end_date, exchange):
        """
        Do download the month data by exchange

        please refer the following link for more details
        https://akshare.akfamily.xyz/data/futures/futures.html#id53
        """
        retry = 0

        while retry <= 5:
            try:
                df = ak.get_futures_daily(
                    start_date=start_date,
                    end_date=end_date,
                    market=exchange)
                # return the result if success
                return df
            # pylint: disable=broad-except
            except Exception:
                retry += 1
                msg = (f"failed download {exchange} {start_date}" +
                       f"-{end_date}, retry {retry} times")
                logger.warning(msg)

            # sleep a few seconds to avoid being blocked by server side.
            time.sleep(10)

        msg = f"failed download {exchange} {start_date}-{end_date}"
        logger.error(msg)
        # raise exception after 5 times retry
        raise exception.DownloadDataError

    def download(self):
        """download all the data."""
        raise NotImplementedError


class FullCNFutureToFileFromAKShare(CNFutureFromAKShare):
    """download all the full data by exchange."""

    def __init__(self, exchanges, dst_dir):
        super().__init__(exchanges)
        self.dst_dir = dst_dir

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

    def download_full_data_by_exchange(self, exchange):
        """download the full data by exchange"""

        # make exchange directory if not exists.
        dst_dir = os.path.join(self.dst_dir, exchange)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)

        start_year = self.exchanges[exchange]["start_year"]
        end_year = self.exchanges[exchange]["end_year"]
        months = self.get_months(start_year, end_year)

        # download the month data
        for start_date, end_date in months:
            file_path = os.path.join(dst_dir, f"{start_date}-{end_date}.csv")

            # skip download if the file already exists
            # the download progress take a very long time.
            if os.path.exists(file_path):
                continue

            # download the file
            msg = f"try to download {exchange} {start_date}-{end_date}"
            logger.info(msg)

            df = self.download_data_by_period(
                start_date,
                end_date,
                exchange)

            if df is not None and len(df) > 0:
                # write to the file if it's not a empty data
                df.to_csv(file_path)
                msg = f"download {exchange} {start_date}-{end_date} success"
                logger.info(msg)
            else:
                msg = f"empty data for {exchange} {start_date}-{end_date}"
                logger.info(msg)

            # sleep a few seconds to avoid being blocked by server side.
            time.sleep(10)

    def download(self):
        """download all the data."""
        for exchange in self.exchanges:
            logger.info("start to download %s contracts", exchange)
            self.download_full_data_by_exchange(exchange)
            logger.info("%s contracts download finished", exchange)


class DeltaCNFutureFromAKShare(CNFutureFromAKShare):
    """download latest delta data by exchange"""

    def __init__(self, exchanges, delta=30):
        super().__init__(exchanges)
        self.delta = delta

    # Attention for the data download in the day!
    #
    # At 13:00: the data in CFFEX, CZCE, DCE and GFEX it empty. However
    # the data in SHFE, INE it not empty, only the close price is nan.
    #
    # At 18:00 & 20:00: it's able to download today's daily data within
    # CFFEX, CZCE, DCE, GFEX, INE, SHFE
    #
    # Note, for zero volume contract
    # CZCE: open, high, low, close are 0
    # DCE/GFEX: open, high, low is 0, close is the same as yesterday.
    # INE/SHFE: open, high, low is nan, close is the same as yesterday.
    def download_delta_data_by_exchange(self, exchange):
        """download the full data by exchange"""
        delta = self.delta
        interval = 30
        t = util_calendar.decision_regard_date()

        dfs = []

        while delta >= interval:
            # prepare the parameters
            end_date = f"{t.year}{t.month:02d}{t.day:02d}"
            start = t + datetime.timedelta(days=-interval)
            start_date = f"{start.year}{start.month:02d}{start.day:02d}"
            # download the data
            df = self.download_data_by_period(start_date, end_date, exchange)
            dfs.append(df)
            # update the value
            delta -= interval
            t = start

        if delta > 0:
            # prepare the data
            end_date = f"{t.year}{t.month:02d}{t.day:02d}"
            start = t + datetime.timedelta(days=-delta)
            start_date = f"{start.year}{start.month:02d}{start.day:02d}"

            # download and update the value
            df = self.download_data_by_period(start_date, end_date, exchange)
            dfs.append(df)

        if len(dfs) == 0:
            return None

        return pd.concat(dfs)

    def download(self):
        """download all the data."""
        dfs = []
        for exchange in self.exchanges:
            logger.info("start to download %s contracts", exchange)
            df = self.download_delta_data_by_exchange(exchange)
            if df is None:
                logger.warning("exchange %s empty contracts", exchange)
                continue
            dfs.append(df)
            logger.info("%s contracts download finished", exchange)

        if len(dfs) == 0:
            return None

        return pd.concat(dfs)


class DeltaCNFutureSymbolsFromAKShare:
    """download all the symbols data by exchanges"""
    def __init__(self, exchanges):
        self.exchanges = exchanges

    def get_symbols_expire(self):
        """get all the symbols expire data."""
        ret = {}
        for exchange in self.exchanges:
            logger.info("start to download %s symbols details", exchange)
            df = self.get_symbol_details_by_exchange(exchange)
            symbols_expire = self.get_symbols_expire_from_df(df, exchange)

            for symbol, expire in symbols_expire.items():
                ret[symbol] = expire
            logger.info("finish download %s symbols details", exchange)

        return ret

    def get_symbol_details_by_exchange(self, exchange):
        """get all the symbols details data by exchange."""

        if exchange == types.SHFE:
            getter = ak.futures_contract_info_shfe
        elif exchange == types.INE:
            getter = ak.futures_contract_info_ine
        elif exchange == types.CFFEX:
            getter = ak.futures_contract_info_cffex
        elif exchange == types.CZCE:
            getter = ak.futures_contract_info_czce
        elif exchange == types.GFEX:
            getter = ak.futures_contract_info_gfex
        elif exchange == types.DCE:
            getter = ak.futures_contract_info_dce
        else:
            raise exception.ExchangeNotSupportedError

        if exchange in (types.GFEX, types.DCE):
            return self.do_getter(getter, exchange)

        return self.do_getter_with_date_fallback(getter, exchange)

    @staticmethod
    def do_getter(getter, exchange):
        """get the symbol without date parameter."""
        retry = 1

        while retry < 5:
            try:
                df = getter()
                return df
            # pylint: disable=broad-except
            except Exception:
                logger.warning(
                    "failed download %s symbol details, retry %d times",
                    exchange, retry)
                retry += 1
            # sleep a few seconds to avoid being blocked by server side.
            time.sleep(5)

        # raise exception after 5 times retry
        raise exception.DownloadDataError

    def do_getter_with_date_fallback(self, getter, exchange):
        """get the symbol with date parameter."""
        # set a larger retry time due to the long holiday like
        # spring festival and cn national day.
        retry = 1
        t = datetime.datetime.now()
        while retry < 15:
            try:
                date = f"{t.year}{t.month:02d}{t.day:02d}"
                df = getter(date=date)
                return df
            # pylint: disable=broad-except
            except Exception:
                logger.warning(
                    "failed download %s symbol details, retry %d times",
                    exchange, retry)
                t = t + datetime.timedelta(days=-1)
                retry += 1
            # sleep a few seconds to avoid being blocked by server side.
            time.sleep(5)

        # raise exception after 5 times retry
        raise exception.DownloadDataError

    def get_symbols_expire_from_df(self, df, exchange):
        """get the symbols details from dataframe."""
        symbols_details = {}
        for _, row in df.iterrows():
            symbol = row["合约代码"]
            # black magic in some exchange, sucks.
            symbol = symbol.replace(" ", "")
            expire = None

            # get the expire date according to the exchange.
            if exchange in (types.SHFE, types.INE):
                expire = row["到期日"]
            elif exchange in (types.CFFEX, types.DCE):
                expire = row["最后交易日"]
            elif exchange == types.CZCE:
                # Suck CZCE again, the exception will be raised in someday!
                expire_str = row["最后交易日待国家公布2025年节假日安排后进行调整"]
                expire = datetime.datetime.strptime(expire_str, "%Y-%m-%d")
            elif exchange == types.GFEX:
                expire = row["最后交易日"]

            if expire is None:
                raise exception.DataInvalidExpireError
            symbols_details[symbol] = expire

        return symbols_details
