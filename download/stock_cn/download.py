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

"""Download the cn stock data from baostock and yahoo finance."""

import datetime
import os

import baostock as bs
import pandas as pd
import yfinance as yf


def covert_to_yahoo_codes(df):
    """
    covert_to_yahoo_codes covert the baostock code to yahoo finance code.

    :param df of stock list downloading from baostock
    :return code list regards to yahoo finance code
    """

    codes = list(set(df.code.tolist()))

    sticker_codes = []
    for code in codes:
        # covert the code format from baostock to yahoo finance
        code = code.upper()
        prefix = code[0:2]
        number_code = code[3:]

        if prefix == "SH":
            yahoo_code = f"{number_code}.SS"
        elif prefix == "SZ":
            yahoo_code = f"{number_code}.SZ"
        else:
            yahoo_code = f"{number_code}.SS"

        sticker_codes.append(yahoo_code)

    return sticker_codes


def get_csi300_date_list():
    """
    get_csi300_date_list return the date list for csi 300

    csi300 start from 2005-04-08, and every half year this constituents will
    be updated at June and December.

    :return date list of csi300
    """
    date_list = []
    for month in range(5, 13):
        date = f"2005-{month:02d}-01"
        date_list.append(date)

    for year in range(2006, datetime.datetime.now().year):
        for month in range(1, 13):
            date = f"{year}-{month:02d}-01"
            date_list.append(date)

    for month in range(1, datetime.datetime.now().month + 1):
        year = datetime.datetime.now().year
        date = f"{year}-{month:02d}-01"
        date_list.append(date)

    return date_list


def get_zz500_date_list():
    """
    get_zz500_date_list return the date list for zz500

    zz500 start from 2004-12-31, and every half year this constituents will
    be updated at June and December.

    :return date list of zz500
    """
    date_list = []
    for year in range(2005, datetime.datetime.now().year):
        for month in range(1, 13):
            date = f"{year}-{month:02d}-01"
            date_list.append(date)

    for month in range(1, datetime.datetime.now().month + 1):
        year = datetime.datetime.now().year
        date = f"{year}-{month:02d}-01"
        date_list.append(date)

    return date_list


def get_csi300_list():
    """
    get csi300 list in every month since 2005-04.
    """

    csi300_list = []

    date_list = get_csi300_date_list()
    for date in date_list:
        rs = bs.query_hs300_stocks(date)
        while (rs.error_code == '0') & rs.next():
            csi300_list.append(rs.get_row_data())

    df = pd.DataFrame(csi300_list, columns=rs.fields)
    return df


def get_zz500_list():
    """
    get zz500 list in every month since 2005-01.
    """

    zz500_list = []

    date_list = get_zz500_date_list()
    for date in date_list:
        rs = bs.query_zz500_stocks(date)
        while (rs.error_code == '0') & rs.next():
            zz500_list.append(rs.get_row_data())

    df = pd.DataFrame(zz500_list, columns=rs.fields)
    return df


def download_sticker_from_yahoo(name):
    """
    download sticker from yahoo finance

    :param name: name of stock
    :return: dataframe of sticker
    """

    df = yf.download(name, period="max")
    df = df.xs(key=name, axis=1, level="Ticker")
    df["code"] = name
    return df


def get_daily_stock(stock_list_df):
    """
    get daily stock

    :param stock_list_df:
    :return: dataframe of daily stock
    """
    df = pd.DataFrame()

    codes = covert_to_yahoo_codes(stock_list_df)
    for code in codes:
        df = pd.concat([df, download_sticker_from_yahoo(code)])

    return df


if "__main__" == __name__:

    # TODO(wsfdl), fixme, some stocks are delisted, for example
    #
    #   ['600001.SS']: YFPricesMissingError('$%ticker%: possibly delisted;
    #   no price data found  (1d 1926-01-28 -> 2025-01-03)')
    #
    # We need to fix this, otherwise it introduce survivorship bias error.

    bs.login()

    # create output directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_dir, "output")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # download csi300 stock daily prices and volumes
    csi300_list_file = os.path.join(output_dir, "csi300_list.csv")
    csi300_list_df = get_csi300_list()
    csi300_list_df.to_csv(csi300_list_file)

    csi300_daily_df = get_daily_stock(csi300_list_df)
    csi300_daily_df.to_csv(os.path.join(output_dir, "csi300_daily.csv"))

    # download zz500 stock daily prices and volumes
    zz500_list_file = os.path.join(output_dir, "zz500_list.csv")
    zz500_list_df = get_zz500_list()
    zz500_list_df.to_csv(zz500_list_file)

    zz500_daily_df = get_daily_stock(zz500_list_df)
    zz500_daily_df.to_csv(os.path.join(output_dir, "zz500_daily.csv"))
