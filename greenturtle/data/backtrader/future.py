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

"""data feed for future."""


import backtrader as bt
from backtrader.feeds import GenericCSVData
import yfinance as yf

from greenturtle.util import time_util
from greenturtle.util import yf_util
import greenturtle.constants.future as future_const


class FutureCSV(GenericCSVData):
    """Future CSV data feed

    multiplier: the number of units for a future contract.
    margin_ratio: the ratio for margin requirement.
    """

    # Add "multiplier" and "margin_ratio" line to the
    # inherited ones from the base class
    lines = (
        future_const.MULTIPLIER,
        future_const.MARGIN_RATIO
    )

    params = (
        (future_const.MULTIPLIER, 7),
        (future_const.MARGIN_RATIO, 8),
    )


class FuturePandasData(bt.feeds.PandasData):
    """Future panda data feed

    multiplier: the number of units for a future contract.
    margin_ratio: the ratio for margin requirement.
    """

    # Add "multiplier" and "margin_ratio" line to the
    # inherited ones from the base class
    lines = (
        future_const.MULTIPLIER,
        future_const.MARGIN_RATIO
    )

    params = (
        (future_const.MULTIPLIER, 7),
        (future_const.MARGIN_RATIO, 8),
    )


# pylint: disable=too-many-positional-arguments,too-many-arguments
def get_data_frame_from_yahoo_finance(
        yahoo_code,
        name=None,
        category=None,
        multiplier=None,
        margin_ratio=None,
        fromdate=None,
        todate=None,
        to_csv=True):
    """
    Get the data frame from yahoo finance and convert it to the format
    expected by backtrader.
    """

    # download the data from yahoo finance
    df = yf.download(yahoo_code, period="max", start=fromdate, end=todate)

    # removing the multi-index column
    df = df.xs(key=yahoo_code, axis=1, level="Ticker")
    # rename the columns
    df = yf_util.rename_yf_column(df)

    if to_csv:
        # format the datetime index for csv
        df.index = df.index.map(lambda x: x.strftime(time_util.DEFAULT_FORMAT))

    # add the yahoo code as a column
    df[future_const.YAHOO_CODE] = yahoo_code

    # add name and category as columns
    if name is not None:
        df["name"] = name
    if category is not None:
        df["category"] = category

    # add contract unit and margin requirement ratio as columns
    if multiplier is not None:
        df[future_const.MULTIPLIER] = multiplier
    if margin_ratio is not None:
        df[future_const.MARGIN_RATIO] = margin_ratio

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
        timeframe=timeframe,
        datatime=0,
        open=5,
        high=3,
        low=4,
        close=2,
        volume=6,
        multiplier=10,
        margin_ratio=11,
        openinterest=None,
        plot=False,
        fromdate=fromdate,
        todate=todate,
    )

    return data


# pylint: disable=too-many-positional-arguments,too-many-arguments
def get_feed_from_yahoo_finance(
        yahoo_code,
        name=None,
        category=None,
        multiplier=None,
        margin_ratio=None,
        fromdate=None,
        todate=None):
    """
    Get the data feed from yahoo finance and convert it to the format
    expected by backtrader.
    """

    df = get_data_frame_from_yahoo_finance(
        yahoo_code,
        name=name,
        category=category,
        multiplier=multiplier,
        margin_ratio=margin_ratio,
        fromdate=fromdate,
        todate=todate,
        to_csv=False)

    # pylint: disable=too-many-function-args,unexpected-keyword-arg
    data = FuturePandasData(
        name=name,
        dataname=df,
        timeframe=bt.TimeFrame.Days,
        open=4,
        high=2,
        low=3,
        close=1,
        volume=5,
        multiplier=9,
        margin_ratio=10,
        openinterest=None,
        plot=False,
        fromdate=fromdate,
        todate=todate,
    )

    return data
