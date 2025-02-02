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

import greenturtle.data.backtrader.future as future_data
from greenturtle.simulator.backtrader import simulator
from greenturtle.stragety.backtrader import ema


# pylint: disable=R0801
DATA_DIR = "../../download/future_us/output/main"
NAME = "HG"
CATEGORY_NAME = "metal"


if __name__ == '__main__':

    s = simulator.Simulator()

    # get the data
    todate = datetime.datetime(2024, 12, 31)
    filename = os.path.join(DATA_DIR, f"{CATEGORY_NAME}/{NAME}.csv")
    data = future_data.get_feed_from_csv_file(NAME, filename, todate=todate)
    s.add_data(data, NAME)

    # add strategy
    s.add_strategy(ema.EMA)

    # do simulate
    s.do_simulate()
