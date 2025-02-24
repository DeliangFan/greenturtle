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

from datetime import datetime
import time

import pandas as pd

from greenturtle.constants.future import types
from greenturtle.constants.future import varieties
from greenturtle.db import api as dbapi
from greenturtle.data.download import future
from greenturtle.data.preprocess import continuous_contract
from greenturtle.data import transform
from greenturtle import exception
from greenturtle.util.logging import logging
from greenturtle.util import util


logger = logging.get_logger()


class Server:
    """online trading server"""
    def __init__(self, conf):
        self.conf = conf
        self.dbapi = dbapi.DBAPI(self.conf.db)

    def start(self):
        """start server"""
        self.synchronize_delta_contract()
        self.synchronize_delta_continuous_contract()

        while True:
            print("I am serving, heartbeat!")
            time.sleep(60)

    def synchronize_delta_contract(self):
        """synchronize delta data."""
        if (
                (self.conf.country == types.CN) and
                (self.conf.source == types.AKSHARE)
        ):
            symbol_loader = future.DeltaCNFutureSymbolsFromAKShare(
                types.CN_EXCHANGES)
            symbols_expire = symbol_loader.get_symbols_expire()
            logger.info("get symbols expire success")

            for exchange in types.CN_EXCHANGES:
                # load data by exchange
                loader = future.DeltaCNFutureFromAKShare([exchange], 7)
                df = loader.download()

                logger.info("start insert %s delta data to db", exchange)
                # do insert to database
                for _, row in df.iterrows():
                    self._synchronize_one_contract(row,
                                                   symbols_expire,
                                                   exchange)

                logger.info("insert %s delta data to db success", exchange)
        else:
            raise NotImplementedError

    def synchronize_delta_continuous_contract(self):
        """synchronize delta continuous contract."""
        if (
                (self.conf.country == types.CN) and
                (self.conf.source == types.AKSHARE)
        ):
            for group in varieties.CN_VARIETIES.values():
                for variety in group:
                    c = continuous_contract.DeltaContinuousContract(
                        variety, self.conf.source, self.conf.country,
                        self.dbapi)
                    c.generate()
        else:
            raise NotImplementedError

    def _synchronize_one_contract(self, row, symbols_expire, exchange):
        """synchronize one contract."""
        # format the field
        date = datetime.strptime(str(row.date), types.DATE_FORMAT)
        row = transform.pd_row_nan_2_none(row)
        row = transform.pd_row_emptystring_2_none(row)
        group = util.get_group(
            row.variety,
            varieties.CN_VARIETIES)

        # skip the variety without group, most of the varieties
        # are filtered due to low volume or low quality data.
        if group is None:
            return

        # format the values field
        values = row.to_dict()
        if "turnover" in values and types.TURN_OVER not in values:
            values[types.TURN_OVER] = values["turnover"]
        self._set_symbol(values, row.symbol, symbols_expire)

        # validate before insert to database
        self._validate(row, values)

        contract = self.dbapi.contract_get_by_constraint(
            date, row.symbol, row.variety, types.AKSHARE, types.CN)
        if contract is not None:
            logger.info("%s %s already exists, skip", date, row.symbol)
            return

        logger.info("insert %s %s to database", date, row.symbol)
        # insert to database
        self.dbapi.contract_create(
            date, row.symbol, row.variety, types.AKSHARE,
            types.CN, exchange, group, values)

    def _validate(self, row, values):
        """validate data"""
        # it is very dangerous for 0 close price since close price
        # is used across all the trading progress.
        close_zero = row.close == 0
        open_nan_zero = row.open != 0 and not pd.isnull(row.open)
        high_nan_zero = row.high != 0 and not pd.isnull(row.high)
        low_nan_zero = row.low != 0 and not pd.isnull(row.low)

        if close_zero and (
                open_nan_zero or high_nan_zero or low_nan_zero):
            raise exception.DataPriceInvalidTypeError

        if pd.isnull(row.close):
            raise exception.DataPriceInvalidTypeError

        # expire is also very important since we use it for rolling
        # contracts
        if types.EXPIRE not in values:
            raise exception.DataInvalidExpireError

        if values[types.EXPIRE] is None:
            raise exception.DataInvalidExpireError

    def _set_symbol(self, values, symbol, symbols_expire):
        """set symbol"""
        if symbol in symbols_expire:
            values[types.EXPIRE] = symbols_expire[symbol]
            return

        # black magic from the exchange, they use upper or lower
        # case chars, the little greenturtle sucks.
        lower = symbol.lower()
        if lower in symbols_expire:
            values[types.EXPIRE] = symbols_expire[lower]
            return
        # sucks again.
        upper = symbol.upper()
        if upper in symbols_expire:
            values[types.EXPIRE] = symbols_expire[upper]
            return

        msg = f"failed get expire for {symbol} from online, will try db"
        logger.warning(msg)
        contracts = self.dbapi.contract_get_all_by_name_source_country(
            symbol, self.conf.source, self.conf.country)

        for contract in contracts:
            if contract.expire is not None:
                values[types.EXPIRE] = contract.expire
                return

        msg = f"failed to get expire for {symbol} from db, raise exception"
        logger.error(msg)
        raise exception.DataInvalidExpireError

    def initialize_broker(self):
        """initialize broker"""

    def initialize_strategy(self):
        """initialize strategy"""

    def initialize_datafeed(self):
        """initialize datafeed"""
