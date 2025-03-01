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
from datetime import date as datetime_date

import backtrader as bt

from greenturtle.constants import types
from greenturtle.constants import varieties
from greenturtle.data.datafeed import db
from greenturtle import exception
from greenturtle.stragety import ema
from greenturtle.util.logging import logging


logger = logging.get_logger()


# pylint: disable=too-many-instance-attributes
class Inference:

    """Inference for online trading based on backtrader."""

    def __init__(self, conf=None, trading_date=datetime_date.today()):
        self.validate_config(conf)

        self.conf = conf
        self.trading_date = trading_date
        self.varieties = varieties.CN_VARIETIES

        self.cerebro = bt.Cerebro()

        self.set_broker()
        self.add_strategy()
        self.add_data()

    def set_broker(self):
        """set broker"""
        # Set our desired cash start
        self.cerebro.broker.setcash(1000000)
        # Set short cash
        self.cerebro.broker.set_shortcash(False)
        # Disable cheat on close
        self.cerebro.broker.set_coc(False)
        # Add a FixedSize sizer according to the stake
        self.cerebro.addsizer(bt.sizers.FixedSize, stake=1)

    # TODO(fixme), better abstraction for broker
    # pylint: disable=R0801
    def get_auto_margin(self, name):
        """get auto margin for future by name."""
        for group in self.varieties.values():
            for future_name, future in group.items():
                if future_name == name:
                    return future[types.AUTO_MARGIN]

        # raise exception if not found
        raise exception.AutoMarginNotFound

    def get_multiplier(self, name):
        """get multiplier for future by name."""
        for group in self.varieties.values():
            for future_name, future in group.items():
                if future_name == name:
                    return future[types.MULTIPLIER]

        # raise exception if not found
        raise exception.MultiplierNotFound

    def set_multiplier_and_auto_margin(self, name):
        """set default commission by name."""
        multiplier = self.get_multiplier(name)
        auto_margin = self.get_auto_margin(name)
        self.cerebro.broker.setcommission(
            mult=multiplier,
            stocklike=False,
            automargin=auto_margin,
            name=name,
        )

    @staticmethod
    def validate_config(conf):
        """Validate config."""
        if hasattr(conf, "risk_factor"):
            risk_factor = conf.risk_factor
            if risk_factor <= 0 or risk_factor > 0.005:
                raise exception.ValidateRiskFactorError

        if hasattr(conf, "group_risk_factors"):
            total_risk_factor = 0
            for factor in conf.group_risk_factors.values():
                if factor <= 0 or factor > 0.02:
                    raise exception.ValidateGroupRiskFactorError
                total_risk_factor += factor
            if total_risk_factor <= 0 or total_risk_factor > 0.08:
                raise exception.ValidateGroupRiskFactorError

        if hasattr(conf, "allow_short"):
            allow_short = conf.allow_short
            if allow_short not in [True, False]:
                raise ValueError("allow_short must be True or False")

        if hasattr(conf, "whitelist"):
            whitelist = conf.whitelist
            if not isinstance(whitelist, (list, tuple)):
                raise ValueError("whitelist must be a list or tuple")

    def add_strategy(self):
        """add strategy to cerebro."""

        risk_factor = varieties.DEFAULT_RISK_FACTOR
        if hasattr(self.conf, "risk_factor"):
            risk_factor = self.conf.risk_factor

        group_risk_factors = varieties.DEFAULT_CN_GROUP_RISK_FACTORS
        if hasattr(self.conf, "group_risk_factors"):
            group_risk_factors = self.conf.group_risk_factors

        allow_short = True
        if hasattr(self.conf, "allow_short"):
            allow_short = self.conf.allow_short

        logger.info("add strategy to cerebro with risk_factor: %s, "
                    "group_risk_factors: %s, allow_short: %s",
                    risk_factor, group_risk_factors, allow_short)

        self.cerebro.addstrategy(ema.EMAEnhanced,
                                 fast_period=10,
                                 slow_period=100,
                                 channel_period=50,
                                 atr_period=100,
                                 risk_factor=risk_factor,
                                 varieties=self.varieties,
                                 group_risk_factors=group_risk_factors,
                                 allow_short=allow_short,
                                 inference=True,
                                 trading_date=self.trading_date)

    def add_data(self):
        """add data to cerebro."""

        whitelist = []
        if hasattr(self.conf, "whitelist"):
            whitelist = self.conf.whitelist

        start_date = datetime(2024, 1, 1)
        end_date = datetime.today()

        # add all data to simulator
        for group in self.varieties.values():
            for name in group:
                if name not in whitelist:
                    continue
                data = db.ContinuousContractDB(db_conf=self.conf.db,
                                               variety=name,
                                               source=self.conf.source,
                                               country=self.conf.country,
                                               start_date=start_date,
                                               end_date=end_date,
                                               plot=False,
                                               padding=True)

                # add the data to simulator
                self.cerebro.adddata(data, name=name)
                self.set_multiplier_and_auto_margin(name)

                logger.info("add data %s to cerebro", name)

    def run(self):
        """run the cerebro to perform really trading."""
        # Print out the starting conditions
        value = self.cerebro.broker.getvalue()
        logger.info("starting trading with value: %.1f", value)

        # Run over everything
        self.cerebro.run()

        # Print out the final result
        value = self.cerebro.broker.getvalue()
        logger.info("finish trading with value: %.1f", value)

    def show_position(self):
        """show position."""
        logger.info("show position")
