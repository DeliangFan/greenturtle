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

"""online trading server"""

import datetime
import time

import schedule

from greenturtle.db import api
from greenturtle.data.deltasyncer import delta_syncer
from greenturtle.inference import inference
from greenturtle.util import calendar
from greenturtle.util.logging import logging
from greenturtle.util.notifier import notifier
from greenturtle.util import util


logger = logging.get_logger()


class Server:
    """
    Online trading server

    Initiate Step
    - start synchronize the delta contract
    - start synchronize the delta continuous contract
    - initiate the inference, show currently hold position and orders

    Enter to a cronjob runs at every 8PM for a trading day
    - synchronize the delta contract
    - synchronize the delta continuous contract
    - initiate the inference and computing the desired holds
    - execute the orders
    - send the trading status including positions, orders.
    """

    def __init__(self, conf, dbapi=None, delta_data_syncer=None):
        self.conf = conf

        if dbapi is None:
            self.dbapi = api.DBAPI(self.conf.db)
        else:
            self.dbapi = dbapi

        if delta_data_syncer is None:
            self.delta_data_syncer = delta_syncer.DeltaSyncer(self.conf,
                                                              self.dbapi)
        else:
            self.delta_data_syncer = delta_data_syncer

        self.notifier = notifier.get_notifier(conf)

    def initialize(self):
        """initialize the server"""
        logger.info("initializing with syncing delta data")
        self.delta_data_syncer.synchronize_delta_contracts()
        self.delta_data_syncer.synchronize_delta_continuous_contracts()
        logger.info("initializing syncing delta data success")

    def trading(self, sleep_time=200):
        """do trading"""

        today = datetime.date.today()
        if not calendar.is_cn_trading_day(today):
            msg = f"skip trading since {today} is not a trading day"
            util.logger_and_notifier(self.notifier, msg)
            return

        util.logger_and_notifier(self.notifier,
                                 "wakeup, it's time to swimming")

        logger.info("prepare syncing the delta data")
        self.delta_data_syncer.synchronize_delta_contracts()
        self.delta_data_syncer.synchronize_delta_continuous_contracts()

        util.logger_and_notifier(self.notifier,
                                 "finish preparing the delta data success")

        trading_day = calendar.decision_regard_date()
        infer = inference.Inference(conf=self.conf,
                                    notifier=self.notifier,
                                    trading_date=trading_day)
        infer.account_overview()
        infer.run()
        time.sleep(sleep_time)
        infer.rolling()
        infer.close()

    def run(self):
        """run server"""

        util.logger_and_notifier(self.notifier, "greenturtle birth to cry.")

        self.initialize()

        # Every day at 12am or 00:00 time bedtime() is called.
        schedule.every().day.at("08:00").do(self.heartbeat)
        schedule.every().day.at("09:31").do(self.trading)
        schedule.every().day.at("21:00").do(self.heartbeat)
        # Loop so that the scheduling task keeps on running all time.
        while True:
            # Checks whether a scheduled task is pending to run or not
            schedule.run_pending()
            logger.info("greenturtle is swimming, breath every minute")
            time.sleep(60)

    def heartbeat(self):
        """heartbeat"""
        util.logger_and_notifier(
            self.notifier, "greenturtle liveness check twice everyday.")
