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

from greenturtle.analyzers import correlation
import greenturtle.constants.stock as stock_const
import greenturtle.data.backtrader.stock as stock_data
from greenturtle.stragety.backtrader import buyhold
from greenturtle.simulator.backtrader import simulator
from greenturtle.util.logging import logging


logger = logging.get_logger()
TICKERS = (
    stock_const.SH50_510050_SS,
    stock_const.CSI300_510300_SS,
    stock_const.CSI500_510500_SS,
    stock_const.Y5_511010_SS,
    stock_const.Y10_511260_SS
)


# pylint: disable=R0801
if __name__ == "__main__":

    c = correlation.Correlation()

    for name in TICKERS:
        s = simulator.Simulator()
        # add the data.
        s.add_data(stock_data.get_feed_from_yahoo_finance(name), name)
        # add strategy
        s.add_strategy(buyhold.BuyHoldStrategy)
        # do simulate
        s.do_simulate()

        # construct daily return dataframe to compute the correlation.
        if s.summary.return_summary is not None:
            c.add_return_summary(name, s.summary.return_summary)

    cc = c.compute_correlation()
    logger.info("\n%s", cc)
