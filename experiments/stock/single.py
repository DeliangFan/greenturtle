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

from datetime import datetime

import greenturtle.constants.stock as stock_constants
import greenturtle.data.backtrader.stock as stock_data
from greenturtle.simulator.backtrader import simulator
from greenturtle.stragety.backtrader import mim


if __name__ == '__main__':

    s = simulator.Simulator()

    fromdate = datetime(2000, 1, 1)
    todate = datetime(2024, 1, 1)

    # add the data.
    data = stock_data.get_feed_from_yahoo_finance(
        stock_constants.QQQ,
        fromdate=fromdate,
        todate=todate)
    s.add_data(data, stock_constants.QQQ)

    # add strategy
    s.add_strategy(mim.MIMStrategy)
    # do simulate
    s.do_simulate()
