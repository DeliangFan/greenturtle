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

from greenturtle.analysis.backtrader import base as base_analysis
from greenturtle.stragety.backtrader import base as base_strategy
from greenturtle.util import panda_util


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
        start_date=None,
        end_date=None):

    """
    Get the data from yahoo finance and convert it to the format
    expected by backtrader.
    """

    df = yf.download(name, period="max", start=start_date, end=end_date)
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

    def __init__(self, tickers, start_date=None, end_date=None):
        self.tickers = tickers
        self.start_date = start_date
        self.end_date = end_date

    def download_from_yfinance(self, name):
        """Download ticker data from yahoo finance."""
        df = yf.download(
            name,
            period="max",
            start=self.start_date,
            end=self.end_date)
        return df

    def transform(self, df, name):
        """
        transform the pandas structure
        - removing the multi-index column
        - renaming column name
        - add datetime as a column
        """

        # Remove multi-index column
        df = df.xs(key=name, axis=1, level="Ticker")

        # rename the columns
        df.rename(columns={"Open": "open"}, inplace=True)
        df.rename(columns={"Adj Close": "adj_close"}, inplace=True)
        df.rename(columns={"Close": "close"}, inplace=True)
        df.rename(columns={"High": "high"}, inplace=True)
        df.rename(columns={"Low": "low"}, inplace=True)
        df.rename(columns={"Volume": "volume"}, inplace=True)

        # add datetime index as a column
        df["datetime"] = df.index
        return df

    def get_ticker_by_name(self, name):
        """Download and transform the ticker by name."""
        df = self.download_from_yfinance(name)
        df = self.transform(df, name)
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
        start_date=None,
        end_date=None):

    """Analyze a number of tickers."""

    panda_util.init_pandas()

    y = YahooFinanceTickers(tickers, start_date=start_date, end_date=end_date)
    df = y.load_tickers()

    return_columns = []
    change_columns = []
    for name in tickers:
        return_columns.append(return_with_name(name))
        change_columns.append(change_with_name(name))

    fig = px.line(df[return_columns], title="ticker overview")
    fig.show()

    df_change = df[change_columns]
    cc = df_change.corr(method="spearman")

    print("correlation coefficient of tickers")
    print(cc)

    start_date = df.index[0]
    if analysis_single:
        for name in tickers:
            do_analysis_ticker(name, start_date, end_date)


def do_analysis_ticker(ticker, start_date=None, end_date=None):
    """Analyze a single ticker."""
    datas = [
        (
            ticker,
            get_backtrader_data_from_yahoo_finance(
                ticker,
                start_date,
                end_date)
        )
    ]

    base_analysis.do_analysis(datas, base_strategy.BaseStrategy)
