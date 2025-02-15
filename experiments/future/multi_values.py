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

from greenturtle.constants.future import varieties
import greenturtle.data.backtrader.future as future_data
from greenturtle.simulator.backtrader import future_simulator
from greenturtle.stragety.backtrader import ema


# pylint: disable=R0801
DATA_DIR = "../../download/future/align/us/"


if __name__ == '__main__':

    s = future_simulator.FutureSimulator(
        plot=True,
        varieties=varieties.US_VARIETIES)

    s.add_strategy(
        ema.EMAEnhanced,
        fast_period=3,
        slow_period=12,
        channel_period=5,
        atr_period=25,
        risk_factor=0.002,
        group_risk_factors=varieties.DEFAULT_GROUP_RISK_FACTORS,
    )

    fromdate = datetime.datetime(2006, 1, 1)
    todate = datetime.datetime(2024, 12, 31)

    # add all data to simulator
    for group in varieties.US_VARIETIES.values():
        for name in group:
            filename = os.path.join(DATA_DIR, f"{name}.csv")
            if not os.path.exists(filename):
                continue

            data = future_data.get_feed_from_csv_file(
                name,
                filename,
                bt.TimeFrame.Days,
                fromdate=fromdate,
                todate=todate)

            # add the data to simulator
            s.add_data(data, name)

            # set the commission according to name
            s.set_default_commission_by_name(name)

    # do simulate
    s.do_simulate()
