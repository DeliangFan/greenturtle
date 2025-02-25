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

"""datafeed from yahoo finance"""

import backtrader as bt
import numpy as np
import yfinance as yf

from greenturtle.constants import types


PANDAS_DATA_CLASS_PARAM = (
    (types.CONTRACT, 0),
    (types.EXPIRE, 1),
    (types.OPEN, 2),
    (types.HIGH, 3),
    (types.LOW, 4),
    (types.CLOSE, 5),
    (types.ORI_OPEN, 6),
    (types.ORI_HIGH, 7),
    (types.ORI_LOW, 8),
    (types.ORI_CLOSE, 9),
    (types.VOLUME, 10),
    (types.TOTAL_VOLUME, 11),
    (types.OPEN_INTEREST, 12),
    (types.TOTAL_OPEN_INTEREST, 13),
    (types.VALID, 14),
)


class FuturePandasData(bt.feeds.PandasData):
    """Future panda data feed."""
    lines = types.CONTINUOUS_LINES
    params = PANDAS_DATA_CLASS_PARAM


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
    df[types.VALID] = True

    # adjust the column order
    df = df[types.CONTINUOUS_COLUMN]

    return df
