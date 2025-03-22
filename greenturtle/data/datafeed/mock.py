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

"""mock datafeed for unittest and e2e tests"""

import datetime

import backtrader as bt
import pandas as pd

from greenturtle.constants import types


PANDAS_DATA_CLASS_PARAM = (
    (types.OPEN, 0),
    (types.HIGH, 1),
    (types.LOW, 2),
    (types.CLOSE, 3),
    (types.VOLUME, 4),
    (types.OPEN_INTEREST, 5),
    (types.VALID, 6),
)


class MockPandasData(bt.feeds.PandasData):
    """Future panda data feed."""
    lines = types.CONTINUOUS_LINES
    params = PANDAS_DATA_CLASS_PARAM

    def __init__(self):
        super().__init__()
        self.name = "mock"

    def get_name(self):
        """return data name"""
        return self.name


def get_mock_dataframe():
    """return a mock dataframe"""

    # create the mock data for datetime, volume, open interest and valid
    datetime_columns = []
    volume_columns = []
    open_interest_columns = []
    valid_columns = []
    start_date = datetime.datetime(2020, 1, 1)
    for i in range(200):
        date = start_date + datetime.timedelta(days=i)
        datetime_columns.append(date)
        volume_columns.append(100)
        open_interest_columns.append(100)
        valid_columns.append(1)

    # create the mock data for price
    open_columns = []
    high_columns = []
    low_columns = []
    close_columns = []
    for i in range(150):
        open_columns.append(10 + 0.2 * i)
        high_columns.append(10 + 0.4 * i)
        low_columns.append(10 + 0.1 * i)
        close_columns.append(10 + 0.3 * i)

    for i in range(50):
        open_columns.append(40 - 0.2 * i)
        high_columns.append(40 - 0.1 * i)
        low_columns.append(40 - 0.4 * i)
        close_columns.append(40 - 0.3 * i)

    data = {
        "open": open_columns,
        "high": high_columns,
        "low": low_columns,
        "close": close_columns,
        "volume": volume_columns,
        "open_interest": open_interest_columns,
        "valid": valid_columns,
    }

    columns = [
        "open",
        "high",
        "low",
        "close",
        "volume",
        "open_interest",
        "valid",
    ]

    # Create DataFrame
    df = pd.DataFrame(
        data,
        index=datetime_columns,
        columns=columns,
    )

    return df


# pylint: disable=too-many-positional-arguments,too-many-arguments
def get_mock_datafeed(name="mock"):
    """
    Get the mock data feed expected by backtrader.
    """

    df = get_mock_dataframe()

    # pylint: disable=too-many-function-args,unexpected-keyword-arg
    datafeed = MockPandasData(
        name=name,
        dataname=df,
        timeframe=bt.TimeFrame.Days,
        plot=False,
    )

    return datafeed
