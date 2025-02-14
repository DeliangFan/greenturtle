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
import os
import time

import akshare as ak

from greenturtle import exception
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
      /{market0}
        /{file0}.csv
        /{file1}.csv
      /{market1}
        /{file2}.csv
        ...
    """
    def __init__(self, markets, dst_dir):
        self.markets = markets
        self.dst_dir = dst_dir

    @abc.abstractmethod
    def download(self):
        """download all the data."""
        raise NotImplementedError


class CNFutureFromAKShare(CNFuture):
    """
    FutureCNDownload used for downloading the cn future data from
    exchanges by month.
    """

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

            # sleep a few seconds to avoid being blocked by server side.
            time.sleep(10)

        # raise exception after 5 times retry
        raise exception.DownloadDataError

    def download_data_by_market(self, market):
        """download the data by market"""

        # make market directory if not exists.
        dst_dir = os.path.join(self.dst_dir, market)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)

        start_year = self.markets[market]["start_year"]
        end_year = self.markets[market]["end_year"]
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

            # sleep a few seconds to avoid being blocked by server side.
            time.sleep(10)

    def download(self):
        """download all the data."""
        for market in self.markets:
            logger.info("start to download market %s", market)
            self.download_data_by_market(market)
            logger.info("market %s download finished", market)
