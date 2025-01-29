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

"""data feed for stock"""

import backtrader as bt
import yfinance as yf

from greenturtle.util import yf_util


def get_feed_from_yahoo_finance(
        name,
        fromdate=None,
        todate=None):
    """
    Get the data from yahoo finance and convert it to the format
    expected by backtrader.
    """

    # download the data from yahoo finance
    df = yf.download(name, period="max", start=fromdate, end=todate)

    # removing the multi-index column
    df = df.xs(key=name, axis=1, level="Ticker")

    # rename the columns
    df = yf_util.rename_yf_column(df)

    # pylint: disable=too-many-function-args,unexpected-keyword-arg
    data = bt.feeds.PandasData(
        dataname=df,
        datetime=None,
        # TODO(fixme)adjust the open/high/low
        open=0,
        high=0,
        low=0,
        close=0,
        volume=None,
        openinterest=None,
        plot=False
    )

    return data
