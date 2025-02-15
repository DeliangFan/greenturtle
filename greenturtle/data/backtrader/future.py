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
Data feed for future.

Greenturtle defines the data structure both in the csv file and datafeed,
which means that these download scripts should convert the data into the
desired format so that the cerebro could consume the data with datafeed.

Data structure.
- index, datetime with "%Y%m%d"
- column contract: contract name,
- column expire: expire date
- column open: open price, the open price should be adjusted price
- column high: high price, the high price should be adjusted price
- column low: low price, the low price should be adjusted price
- column close: close price, the close price should be adjusted price
- column ori_open: original open price
- column ori_high: original high price
- column ori_low: original low price
- column ori_close: original close price
- column volume: the amount of volume
- column total_volume: total volume of all contracts
- column open_interest: open interest
- column total_open_interest: total open interest of all contracts
"""


import backtrader as bt
import numpy as np
from backtrader.feeds import GenericCSVData
import yfinance as yf

from greenturtle.constants.future import types


# TODO(fixme), generate automatically
CLASS_PARAM = (
    (types.CONTRACT, 1),
    (types.EXPIRE, 2),
    (types.OPEN, 3),
    (types.HIGH, 4),
    (types.LOW, 5),
    (types.CLOSE, 6),
    (types.ORI_OPEN, 7),
    (types.ORI_HIGH, 8),
    (types.ORI_LOW, 9),
    (types.ORI_CLOSE, 10),
    (types.VOLUME, 11),
    (types.TOTAL_VOLUME, 12),
    (types.OPEN_INTEREST, 13),
    (types.TOTAL_OPEN_INTEREST, 14),
)


class FutureCSV(GenericCSVData):
    """Future CSV data feed"""
    params = CLASS_PARAM


class FuturePandasData(bt.feeds.PandasData):
    """Future panda data feed."""
    params = CLASS_PARAM


# pylint: disable=too-many-positional-arguments,too-many-arguments
def get_data_frame_from_yahoo_finance(
        yahoo_code,
        fromdate=None,
        todate=None):

    """
    Get the data frame from yahoo finance and convert it to the format
    expected by backtrader.
    """

    # download the data from yahoo finance
    df = yf.download(yahoo_code, period="max", start=fromdate, end=todate)

    # removing the multi-index column
    df = df.xs(key=yahoo_code, axis=1, level="Ticker")

    # rename the columns
    df.rename(columns={"Open": types.ORI_OPEN}, inplace=True)
    df.rename(columns={"Close": types.ORI_CLOSE}, inplace=True)
    df.rename(columns={"High": types.ORI_HIGH}, inplace=True)
    df.rename(columns={"Low": types.ORI_LOW}, inplace=True)

    # rename the adjust name
    df.rename(columns={"Adj Close": types.CLOSE}, inplace=True)

    # rename the volume
    df.rename(columns={"Volume": types.VOLUME}, inplace=True)

    # add new price columns, these are for adjusted price
    df[types.OPEN] = np.nan
    df[types.HIGH] = np.nan
    df[types.LOW] = np.nan
    for index, row in df.iterrows():
        factor = row[types.CLOSE] / row[types.ORI_CLOSE]
        # set the open/high/low adjusted price.
        df.at[index, types.OPEN] = row[types.ORI_OPEN] * factor
        df.at[index, types.HIGH] = row[types.ORI_HIGH] * factor
        df.at[index, types.LOW] = row[types.ORI_LOW] * factor

    # the contract/expire/open_interest columns to unknown etc
    df[types.CONTRACT] = np.nan
    df[types.EXPIRE] = np.nan
    df[types.OPEN_INTEREST] = np.nan
    df[types.TOTAL_VOLUME] = np.nan
    df[types.TOTAL_OPEN_INTEREST] = np.nan

    # adjust the column order
    df = df[types.CONTINUOUS_COLUMN]

    return df


def get_feed_from_csv_file(
        name,
        filename,
        timeframe=bt.TimeFrame.Days,
        fromdate=None,
        todate=None):

    """get the US future data from local csv file.

    please make sure that this csv file are create by the function
    get_data_frame_from_yahoo_finance.
    """

    # pylint: disable=R0801
    data = FutureCSV(
        name=name,
        dataname=filename,
        dtformat=types.DATE_FORMAT,
        timeframe=timeframe,
        datatime=0,
        plot=False,
        fromdate=fromdate,
        todate=todate,
    )

    return data


# pylint: disable=too-many-positional-arguments,too-many-arguments
def get_feed_from_yahoo_finance(
        yahoo_code,
        name=None,
        fromdate=None,
        todate=None):
    """
    Get the data feed from yahoo finance and convert it to the format
    expected by backtrader.
    """

    df = get_data_frame_from_yahoo_finance(
        yahoo_code,
        fromdate=fromdate,
        todate=todate)

    # pylint: disable=too-many-function-args,unexpected-keyword-arg
    data = FuturePandasData(
        name=name,
        dataname=df,
        timeframe=bt.TimeFrame.Days,
        plot=False,
        fromdate=fromdate,
        todate=todate,
    )

    return data
