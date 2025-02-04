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

"""Experiment to benchmark the RSI performance on cryptocurrencies."""

import greenturtle.data.backtrader.crypto as crypto_data
from greenturtle.simulator.backtrader import stock_simulator
from greenturtle.stragety.backtrader import ema


# pylint: disable=R0801
DATA_NAME = "../../download/crypto/csv/btc_1d.csv"
CRYPTO_NAME = "btc"


if __name__ == '__main__':

    s = stock_simulator.StockSimulator()
    s.set_commission()

    # add data
    data = crypto_data.get_feed_from_csv_file(CRYPTO_NAME, DATA_NAME)
    s.add_data(data, CRYPTO_NAME)

    # add strategy
    s.add_strategy(ema.EMA)

    s.do_simulate()
