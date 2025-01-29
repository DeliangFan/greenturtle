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

"""Some common functions for stock experiment."""


import backtrader as bt
import pandas as pd
import plotly.express as px
import yfinance as yf

from greenturtle.simulator.backtrader import simulator
from greenturtle.stragety.backtrader import base as base_strategy
from greenturtle.util import panda_util
from greenturtle.util import yf_util
from greenturtle.util.logging import logging


logger = logging.get_logger()


def change_with_name(name):
    """Generate the change column with ticker name."""
    return name + "_change"


def adj_with_name(name):
    """Generate the adjust column with ticker name."""
    return name + "_adjust"


def return_with_name(name):
    """Generate the return column with ticker name."""
    return name + "_return"


def get_backtrader_data_from_yahoo_finance(
        name,
        fromdate=None,
        todate=None):

    """
    Get the data from yahoo finance and convert it to the format
    expected by backtrader.
    """

    df = yf.download(name, period="max", start=fromdate, end=todate)
    df = df.xs(key=name, axis=1, level="Ticker")

    # pylint: disable=too-many-function-args,unexpected-keyword-arg
    data = bt.feeds.PandasData(
        dataname=df,
        datetime=None,
        open=0,
        high=0,
        low=0,
        close=0,
        volume=None,
        openinterest=None,
        plot=False
    )

    return data


class YahooFinanceTickers():

    """
    YahooFinanceTicker download the data and process the data with
    transform, normalization for a number of tickers.

    Download: download sticker data from yahoo finance.
    Transform: transform panda structure by removing the multi-index
        column, and rename column name.

    The output is always stored in a pandas dataframe.
    """

    def __init__(self, tickers, fromdate=None, todate=None):
        self.tickers = tickers
        self.fromdate = fromdate
        self.todate = todate

    def download_from_yfinance(self, name):
        """Download ticker data from yahoo finance."""
        df = yf.download(
            name,
            period="max",
            start=self.fromdate,
            end=self.todate)
        return df

    def get_ticker_by_name(self, name):
        """Download and transform the ticker by name."""
        df = self.download_from_yfinance(name)
        df = yf_util.transform(df, name)
        df = df[["adj_close"]]
        df.rename(columns={"adj_close": adj_with_name(name)}, inplace=True)
        return df

    def get_tickers(self):
        """Get the list of tickers."""
        df_list = []
        for name in self.tickers:
            df = self.get_ticker_by_name(name)
            df_list.append(df)
        return pd.concat(df_list, axis=1, join='inner')

    def add_return_column(self, df, name):
        """Insert the return column."""
        column_adj = adj_with_name(name)
        column_return = return_with_name(name)

        df.insert(
            len(df.columns),
            column_return,
            [0] * len(df),
            allow_duplicates=False)

        base = df[column_adj][0]
        for i in range(len(df)):
            df[column_return].iloc[i] = df[column_adj][i] / base
        return df

    def add_change_column(self, df, name):
        """Insert the change column."""
        column_adj = adj_with_name(name)
        column_change = change_with_name(name)

        df.insert(
            len(df.columns),
            column_change,
            [0] * len(df),
            allow_duplicates=False)

        for i in range(1, len(df)):
            diff = df[column_adj][i] - df[column_adj][i - 1]
            df[column_change].iloc[i] = diff / df[column_adj][i - 1]

        return df

    def add_columns(self, df, name):
        """Insert some columns to a ticker."""
        self.add_return_column(df, name)
        self.add_change_column(df, name)
        return df

    def normalize_tickers(self, df):
        """Normalize all the tickers."""
        for name in self.tickers:
            df = self.add_columns(df, name)
        return df

    def load_tickers(self):
        """Load all the tickers."""
        df = self.get_tickers()
        df = self.normalize_tickers(df)
        return df


def do_analysis(
        tickers,
        analysis_single=False,
        fromdate=None,
        todate=None,
        plot=False):

    """Analyze a number of tickers."""

    panda_util.init_pandas()

    y = YahooFinanceTickers(tickers, fromdate=fromdate, todate=todate)
    df = y.load_tickers()

    return_columns = []
    change_columns = []
    for name in tickers:
        return_columns.append(return_with_name(name))
        change_columns.append(change_with_name(name))

    if plot:
        fig = px.line(df[return_columns], title="ticker overview")
        fig.show()

    df_change = df[change_columns]
    cc = df_change.corr(method="spearman")

    logger.info("correlation coefficient of tickers")
    logger.info("\n%s", cc)

    fromdate = df.index[0]
    if analysis_single:
        for name in tickers:
            do_analysis_ticker(name, fromdate, todate)


def do_analysis_ticker(ticker, fromdate=None, todate=None):
    """Analyze a single ticker."""
    s = simulator.Simulator()

    # add data.
    s.add_data(
        get_backtrader_data_from_yahoo_finance(
            ticker,
            fromdate,
            todate),
        ticker)

    # add strategy
    s.add_strategy(base_strategy.BaseStrategy)

    # do simulate
    s.do_simulate()
