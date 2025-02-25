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


"""datafeed from csv file"""


import backtrader as bt
from backtrader.feeds import GenericCSVData

from greenturtle.constants import types


CSV_CLASS_PARAM = (
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
    (types.VALID, 15),
)


class FutureCSV(GenericCSVData):
    """Future CSV data feed"""
    lines = types.CONTINUOUS_LINES
    params = CSV_CLASS_PARAM


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
