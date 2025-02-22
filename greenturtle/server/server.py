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

import time
from datetime import datetime

from greenturtle.constants.future import types
from greenturtle.constants.future import varieties
from greenturtle.db import api as dbapi
from greenturtle.data.download import cn_future
from greenturtle.util import util
from greenturtle.util.logging import logging


logger = logging.get_logger()


class Server:
    """online trading server"""
    def __init__(self, conf):
        self.conf = conf
        self.dbapi = dbapi.DBAPI(self.conf.db)

    def start(self):
        """start server"""
        self.synchronize_delta_data()

        while True:
            print("I am serving, heartbeat!")
            time.sleep(60)

    def synchronize_delta_data(self):
        """synchronize delta data."""
        if (
                (self.conf.country == types.CN) and
                (self.conf.source == types.AKSHARE)
        ):
            for exchange in types.CN_EXCHANGES:
                # load data by exchange
                loader = cn_future.CNFutureFromAKShareDelta([exchange], 1)
                df = loader.download()

                msg = f"start insert {exchange} delta data to database"
                logger.info(msg)

                for _, row in df.iterrows():
                    # format the field
                    row = util.nan2none(row)
                    row = util.emptystring2none(row)
                    group = util.get_group(
                        row.variety,
                        varieties.CN_VARIETIES)
                    date = datetime.strptime(str(row.date), types.DATE_FORMAT)

                    # format the values field
                    values = row.to_dict()
                    if "turnover" in values and types.TURN_OVER not in values:
                        values[types.TURN_OVER] = values["turnover"]

                    # insert to database
                    self.dbapi.contract_create(
                        date,
                        row.symbol,
                        row.variety,
                        types.AKSHARE,
                        types.CN,
                        exchange,
                        group,
                        values,
                    )

                msg = f"insert {exchange} delta data to database success"
                logger.info(msg)
        else:
            raise NotImplementedError

    def initialize_broker(self):
        """initialize broker"""

    def initialize_strategy(self):
        """initialize strategy"""

    def initialize_datafeed(self):
        """initialize datafeed"""
