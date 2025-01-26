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

"""Experiment to benchmark trending trading performance on single us future."""

import datetime
import os

import backtrader as bt

from greenturtle.simulator.backtrader import simulator
from greenturtle.stragety.backtrader import macd
from experiments.future import common

# pylint: disable=R0801
DATA_DIR = "../../download/future_us/output"
NAME = "HG"
CATEGORY_NAME = "metal"


if __name__ == '__main__':

    todate = x = datetime.datetime(2024, 12, 31)
    category_dir = os.path.join(DATA_DIR, CATEGORY_NAME)
    filename = os.path.join(DATA_DIR, f"{CATEGORY_NAME}/{NAME}.csv")

    # get the data
    data = common.get_us_future_data_from_csv_file(
        NAME,
        filename,
        bt.TimeFrame.Days,
        todate=todate)
    datas = [(NAME, data)]

    # do analysis
    simulator.do_simulate(datas, macd.RefinedMACDStrategy, plot=True)
