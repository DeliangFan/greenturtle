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

""" Base strategy class for backtrader which implements some basic interface"""

import math

import backtrader as bt

from greenturtle.util.logging import logging


logger = logging.get_logger()


class BaseStrategy(bt.Strategy):

    """ base strategy for backtrader framework."""

    def __init__(self):
        super().__init__()
        self.order = None

    def log(self, txt, dt=None):
        """ Logging function fot this strategy."""
        dt = dt or self.datas[0].datetime.date(0)
        iso_time = dt.isoformat()
        logger.info("%s: %s", iso_time, txt)

    def start(self):
        self.order = None

    def next(self):
        if self.order:
            return

        # not in the market
        if not self.position:
            self.order_target_percent(target=0.99)

    def notify_order(self, order):
        """
        notify order response the order according to the status of the order
        and log the order.
        """
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            # pylint: disable=protected-access
            name, price = order.data._name, order.executed.price
            size, comm = order.executed.size, order.executed.comm
            value = math.fabs(size) * price

            if order.isbuy():
                self.log(
                    f"BUY EXECUTED, name: {name}, price: {price:.2f}, " +
                    f"size: {size:.0f}, value: {value:.2f}, comm: {comm:.2f}"
                )
            elif order.issell():
                self.log(
                    f"SELL EXECUTED, name: {name}, price: {price:.2f}, " +
                    f"size: {size:.0f}, value: {value:.2f}, comm: {comm:.2f}"
                )

            total_value = self.broker.get_value()
            position_size = self.position.size
            position_price = self.position.price
            self.log(
                f"total value: {total_value}, position size: {position_size}" +
                f", position price: {position_price}")

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None
