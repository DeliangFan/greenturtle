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

from greenturtle.constants import types
from greenturtle.constants import varieties
from greenturtle.data.datafeed import db
from greenturtle.backtesting import backtesting
from greenturtle.stragety import ema
from greenturtle.util import config


if __name__ == '__main__':

    RISK_FACTOR = 0.002
    group_risk_factors = varieties.DEFAULT_CN_GROUP_RISK_FACTORS
    varieties_map = varieties.CN_VARIETIES

    conf = config.load_config("/etc/greenturtle/greenturtle.yaml")
    s = backtesting.BackTesting(plot=True, varieties=varieties_map)

    s.add_strategy(
        ema.EMAEnhanced,
        fast_period=10,
        slow_period=100,
        channel_period=50,
        atr_period=100,
        risk_factor=RISK_FACTOR,
        varieties=varieties_map,
        group_risk_factors=group_risk_factors,
        allow_short=True,
    )

    start_date = datetime.datetime(2006, 1, 1)
    end_date = datetime.datetime(2024, 12, 31)

    # add all data to simulator
    for group in varieties_map.values():
        for name in group:

            if name not in conf.whitelist:
                continue

            data = db.ContinuousContractDB(db_conf=conf.db,
                                           variety=name,
                                           source=types.AKSHARE,
                                           country=types.CN,
                                           start_date=start_date,
                                           end_date=end_date,
                                           plot=False,
                                           padding=True)

            # add the data to simulator
            s.add_data(data, name)

            # set the commission according to name
            s.set_default_commission_by_name(name)

    # do backtesting
    s.do_backtesting()
