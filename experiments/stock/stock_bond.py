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
from greenturtle.stragety.backtrader import stock_bond
from greenturtle.simulator.backtrader import simulator
from experiments.stock import common


if __name__ == '__main__':
    datas = [
        (
            stock_const.STOCK,
            common.get_backtrader_data_from_yahoo_finance(
                stock_const.VFIAX,
            )
         ),
        (
            stock_const.BOND,
            common.get_backtrader_data_from_yahoo_finance(stock_const.TLT)
         ),
    ]

    simulator.do_simulate(datas, stock_bond.BalancedStockAndBondStrategy)
