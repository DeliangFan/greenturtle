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

"""Analysis the profit about us ETF."""


import greenturtle.constants.stock as stock_const
from experiments.stock import common


TICKERS = (
    stock_const.SH50_510050_SS,
    stock_const.CSI300_510300_SS,
    stock_const.CSI500_510500_SS,
    stock_const.Y5_511010_SS,
    stock_const.Y10_511260_SS
)


if __name__ == "__main__":
    common.do_analysis(TICKERS)
