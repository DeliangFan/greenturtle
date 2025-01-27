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

"""Experiment to benchmark the trending trading performance on us futures."""

import datetime
import os

import backtrader as bt
import pandas as pd

from greenturtle.simulator.backtrader import simulator
from greenturtle.stragety.backtrader import ema
from greenturtle.util.constants import constants_future
from greenturtle.util.logging import logging
from experiments.future import common


logger = logging.get_logger()
# pylint: disable=R0801
DATA_DIR = "../../download/future_us/output"
SKIP_LIST = ("6B", "6J", "DX", "6E", "ZN", "ZT")


if __name__ == '__main__':

    df = pd.DataFrame()
    fromdate = datetime.datetime(2004, 1, 1)
    todate = x = datetime.datetime(2024, 12, 31)
    for category_name, category_value in constants_future.FUTURE.items():
        category_dir = os.path.join(DATA_DIR, category_name)
        for name, future in category_value.items():
            if name in SKIP_LIST:
                continue
            # get the data
            filename = os.path.join(DATA_DIR, f"{category_name}/{name}.csv")
            data = common.get_us_future_data_from_csv_file(
                name,
                filename,
                bt.TimeFrame.Days,
                fromdate=fromdate,
                todate=todate)
            datas = [(name, data)]

            # do analysis
            s = simulator.do_simulate(
                datas,
                ema.EMA,
                commission=0.001,
                slippage=0.000,
                plot=False)

            # construct the result and append it to the dataframe
            row = {
                "name": [name],
                "category": [category_name],
                "total_return": [s.total_return],
                "annual_return": [s.annual_return],
                "sharpe_ratio": [s.sharpe_ratio],
                "leverage": [s.leverage],
                "max_draw_down": [s.max_draw_down],
                "total_trade": [s.total],
                "won_ratio": [s.won_ratio],
            }

            new_df = pd.DataFrame(row)
            df = pd.concat([df, new_df])

    logger.info("\n%s", df.to_string())

    # TODO(wsfdl), add corelation analysis for different future within
    # same strategy
