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

"""Analysis the profit by combining stock and bond."""

import greenturtle.constants.stock as stock_const
import greenturtle.data.backtrader.stock as stock_data
from greenturtle.stragety.backtrader import stock_bond
from greenturtle.simulator.backtrader import stock_simulator


if __name__ == '__main__':

    s = stock_simulator.StockSimulator()
    s.set_commission()

    # add the bond and stock data.
    data = stock_data.get_feed_from_yahoo_finance(stock_const.VFIAX)
    s.add_data(data, stock_const.STOCK)

    data = stock_data.get_feed_from_yahoo_finance(stock_const.TLT)
    s.add_data(data, stock_const.BOND)

    # add strategy
    s.add_strategy(stock_bond.BalancedStockAndBondStrategy)

    # do simulate
    s.do_simulate()
