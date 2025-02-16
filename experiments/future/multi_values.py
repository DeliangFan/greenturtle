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


if __name__ == '__main__':

    DATA_DIR = "../../download/future/align/cn/"
    RISK_FACTOR = 0.004
    group_risk_factors = varieties.DEFAULT_CN_GROUP_RISK_FACTORS
    varieties_map = varieties.CN_VARIETIES

    s = future_simulator.FutureSimulator(
        plot=True,
        varieties=varieties_map)

    s.add_strategy(
        ema.EMAEnhanced,
        fast_period=10,
        slow_period=100,
        channel_period=50,
        atr_period=100,
        risk_factor=RISK_FACTOR,
        varieties=varieties_map,
        group_risk_factors=group_risk_factors,
    )

    fromdate = datetime.datetime(2006, 1, 1)
    todate = datetime.datetime(2024, 12, 31)

    # add all data to simulator
    for group in varieties_map.values():
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
