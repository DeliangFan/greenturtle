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
import os

import akshare as ak
import pandas as pd

from greenturtle.util.logging import logging


logger = logging.get_logger()
CN_MARKETS = ("CFFEX", "SHFE", "INE", "CZCE", "DCE", "GFEX")


def get_month_list():
    """get the month list with start date and end date."""

    month_list = []

    for year in range(1990, 2025):
        for month in range(1, 13):
            # use calendar.mongthrange to get month last day
            monthrange = calendar.monthrange(year, month)
            start_day = f"{year}{month:02d}01"
            end_day = f"{year}{month:02d}{monthrange[1]:02d}"

            month_list.append((start_day, end_day))

    return month_list


def download_cn_future_by_market(market):
    """ download the cn future data from exchanges by market."""

    df = pd.DataFrame()

    month_list = get_month_list()
    for month in month_list:
        logger.info("start to download %s %s-%s", market, month[0], month[1])
        try:
            # please refer the following link for more details
            # https://akshare.akfamily.xyz/data/futures/futures.html#id53
            daily_df = ak.get_futures_daily(
                start_date=month[0],
                end_date=month[1],
                market=market)
            df = pd.concat([df, daily_df])
            logger.info(
                "download %s %s-%s success", market, month[0], month[1])
        except (Exception, ) as e:  # pylint: disable=broad-except
            logger.error(e)

    return df


if __name__ == '__main__':
    # create output directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_dir, "output")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # download future data and write to csv file
    for cn_market in CN_MARKETS:
        logger.info("start to download market %s", cn_market)
        data = download_cn_future_by_market(cn_market)
        data.to_csv(os.path.join(output_dir, f"{cn_market}.csv"))
        logger.info("market %s download finished", cn_market)
