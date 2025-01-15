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

"""utils for yahoo finance"""

import yfinance as yf


def download_with_max_period(yahoo_code):
    """download the data with max period"""
    df = yf.download(yahoo_code, period="max")
    return df


def transform(df, yahoo_code):
    """
    transform the pandas structure
    - removing the multi-index column
    - renaming column name
    - add datetime as a column
    """

    df = df.xs(key=yahoo_code, axis=1, level="Ticker")

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
