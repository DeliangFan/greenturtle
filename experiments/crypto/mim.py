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

"""Experiment to benchmark the MIM performance on cryptocurrencies."""

import backtrader as bt

from greenturtle.simulator.backtrader import simulator
from greenturtle.stragety.backtrader import mim
from experiments.crypto import common

# pylint: disable=R0801
DATA_NAME = "../../download/crypto/csv/eth_1d.csv"
CRYPTO_NAME = "eth"


if __name__ == '__main__':
    data = common.get_crypto_data_from_csv_file(
        CRYPTO_NAME, DATA_NAME, bt.TimeFrame.Days)

    s = simulator.Simulator()
    s.add_data(data, CRYPTO_NAME)
    s.add_strategy(mim.MIMStrategy)
    s.do_simulate()
