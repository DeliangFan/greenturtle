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

"""Experiment print the kline for analysis."""

import backtrader as bt

from greenturtle.constants import types
from greenturtle.data.datafeed import db
from greenturtle.stragety import buyhold
from greenturtle.util import config


if __name__ == '__main__':
    conf = config.load_config("/etc/greenturtle/greenturtle.yaml")
    cerebro = bt.Cerebro()

    VARIETY = "A"
    data = db.ContinuousContractDB(db_conf=conf.db,
                                   variety=VARIETY,
                                   source=types.AKSHARE,
                                   country=types.CN,
                                   plot=True,
                                   padding=False)

    cerebro.adddata(data, VARIETY)
    cerebro.addstrategy(buyhold.BuyHoldStrategy)
    cerebro.run()
    cerebro.plot()
