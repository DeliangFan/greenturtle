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

"""Inference for online trading."""

from datetime import datetime

import backtrader as bt

from greenturtle.constants import types
from greenturtle.util.logging import logging


logger = logging.get_logger()


# pylint: disable=too-many-instance-attributes
class Inference:

    """Inference for online trading based on backtrader."""

    def __init__(self, trading_date=datetime.today(), varieties=None):
        self.varieties = varieties
        self.trading_date = trading_date
        self.cerebro = bt.Cerebro()

    def add_strategy(self, strategy, *args, **kwargs):
        """add strategy to cerebro."""
        kwargs[types.TRADING_DATE] = self.trading_date
        self.cerebro.addstrategy(strategy, *args, **kwargs)

    def add_data(self, data, name=None):
        """add data to cerebro."""
        self.cerebro.adddata(data, name=name)

    def run(self):
        """
        run the cerebro to perform backtesting.

        # Print out the starting conditions
        value = self.cerebro.broker.getvalue()
        logger.info("starting portfolio value: %.2f", value)

        # Run over everything
        self.cerebro.run()

        # Print out the final result
        value = self.cerebro.broker.getvalue()
        logger.info("final Portfolio Value: %.2f", value)
        """
        logger.info("run today's trading")

    def show_position(self):
        """show position."""
