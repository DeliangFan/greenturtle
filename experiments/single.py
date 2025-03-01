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

from greenturtle.constants import types
from greenturtle.constants import varieties
from greenturtle.data.datafeed import db
from greenturtle.backtesting import backtesting
from greenturtle.stragety import ema
from greenturtle.util import config


if __name__ == '__main__':

    VARIETY = "IF"
    conf = config.load_config("/etc/greenturtle/greenturtle.yaml")

    s = backtesting.BackTesting(varieties=varieties.CN_VARIETIES)
    s.set_default_commission_by_name(VARIETY)

    # get the data
    start_date = datetime.datetime(2005, 1, 1)
    end_date = datetime.datetime(2024, 12, 31)

    # pylint: disable=R0801
    data = db.ContinuousContractDB(db_conf=conf.db,
                                   variety=VARIETY,
                                   source=types.AKSHARE,
                                   country=types.CN,
                                   start_date=start_date,
                                   end_date=end_date,
                                   padding=True)
    s.add_data(data, VARIETY)

    # add strategy
    s.add_strategy(ema.EMAEnhanced,
                   varieties=varieties.CN_VARIETIES,
                   risk_factor=0.02)

    # do backtesting
    s.do_backtesting()
