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

from greenturtle.constants import varieties
from greenturtle.data.datafeed import csv
from greenturtle.simulator import simulator
from greenturtle.stragety import ema


# pylint: disable=R0801
DATA_DIR = "../download/align/us/"
NAME = "GC"


if __name__ == '__main__':

    s = simulator.Simulator(varieties=varieties.US_VARIETIES)
    s.set_default_commission_by_name(NAME)

    # get the data
    fromdate = datetime.datetime(2006, 1, 1)
    todate = datetime.datetime(2024, 12, 31)
    filename = os.path.join(DATA_DIR, f"{NAME}.csv")

    data = csv.get_feed_from_csv_file(
        NAME,
        filename,
        fromdate=fromdate,
        todate=todate)
    s.add_data(data, NAME)

    # add strategy
    s.add_strategy(ema.EMA)

    # do simulate
    s.do_simulate()
