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

"""delta syncer synchronize the delta data."""

import datetime

import pandas as pd

from greenturtle.constants import types
from greenturtle.constants import varieties
from greenturtle.data.download import future
from greenturtle.data.preprocess import continuous_contract
from greenturtle.data import transform
from greenturtle import exception
from greenturtle.util import calendar
from greenturtle.util.logging import logging
from greenturtle.util import util


logger = logging.get_logger()


class DeltaSyncer:
    """
    synchronize delta data including contracts and continuous contracts
    """

    def __init__(self, conf, dbapi):
        self.conf = conf
        self.dbapi = dbapi

    def has_delta_contracts_synced(self):
        """
        check the delta contracts has been synced or not

        1. if today is not trading day, then check the data of the latest
           trading day.
        2. if today is trading day, then check the time. If the trading has
           been closed, then check today's data. If the trading has not been
           closed, then check the data of the latest trading day.

        Then check if every variety has the contract in the trading date
        """
        # the data in the date which is used to make decision.
        decision_date = calendar.decision_regard_date()

        # convert date to datetime
        decision_date_time = datetime.datetime.combine(
            decision_date, datetime.datetime.min.time())

        # prepare parameters
        get = self.dbapi.contract_get_all_by_variety_source_country_since_date
        since = decision_date_time + datetime.timedelta(days=-200)

        for group in varieties.CN_VARIETIES.values():
            for variety in group:
                # contracts need to check
                checks = set()
                contracts = get(variety=variety,
                                source=self.conf.source,
                                country=self.conf.country,
                                date=since)

                for contract in contracts:
                    if contract.expire >= decision_date_time:
                        checks.add(contract.name)

                # check the contracts
                for name in checks:
                    one = self.dbapi.contract_get_by_constraint(
                        date=decision_date_time,
                        name=name,
                        variety=variety,
                        source=self.conf.source,
                        country=self.conf.country,
                    )
                    if not one:
                        logger.warning("%s %s delta contract not synced yet",
                                       name, decision_date_time)
                        return False
        return True

    def synchronize_delta_contracts(self):
        """synchronize delta data."""
        if not (
                (self.conf.country == types.CN) and
                (self.conf.source == types.AKSHARE)
        ):
            raise NotImplementedError

        if self.has_delta_contracts_synced():
            logger.info("skip sync delta contract since already synced")
            return

        symbols_expire = self._get_symbols_expire(types.CN_EXCHANGES)

        df_map = self._get_contract_df_map(types.CN_EXCHANGES)

        # format the contract data
        contracts = self._format_contracts(types.CN_EXCHANGES,
                                           df_map,
                                           symbols_expire)
        if contracts is None:
            logger.warning("skip synchronize delta contracts due to"
                           "empty contract in some exchange")
            return
        if len(contracts) == 0:
            logger.info("skip synchronize delta contract with empty contract")
            return

        self._validate_contracts(contracts)
        self._write_contracts_to_database(contracts)

    @staticmethod
    def _get_symbols_expire(exchanges):
        """get symbols expire"""
        logger.info("start get symbols expire")

        symbol_loader = future.DeltaCNFutureSymbolsFromAKShare(exchanges)
        symbols_expire = symbol_loader.get_symbols_expire()

        logger.info("get symbols expire success")
        return symbols_expire

    @staticmethod
    def _get_contract_df_map(exchanges):
        """get contract dataframe map"""

        logger.info("start get contracts")

        df_map = {}
        # download data from all exchanges, if one of them fails, then
        # exceptions will be raised.
        for exchange in exchanges:
            # load data by exchange
            loader = future.DeltaCNFutureFromAKShare([exchange], 20)
            df_map[exchange] = loader.download()

        logger.info("get contracts success")

        return df_map

    def _format_contracts(self, exchanges, df_map, symbols_expire):
        """format contracts"""
        logger.info("start format contracts")

        contracts = []
        for exchange in exchanges:
            df = df_map[exchange]
            if df is None:
                logger.info("%s empty delta contract", exchange)
                return None

            for _, row in df.iterrows():
                date = datetime.datetime.strptime(str(row.date),
                                                  types.DATE_FORMAT)
                row = transform.pd_row_nan_2_none(row)
                row = transform.pd_row_emptystring_2_none(row)
                group = util.get_group(
                    row.variety,
                    varieties.CN_VARIETIES)

                # skip the variety without group, most of the varieties
                # are filtered due to low volume or low quality data.
                if group is None:
                    continue

                # format the values field
                contract = row.to_dict()
                if "turnover" in contract and types.TURN_OVER not in contract:
                    contract[types.TURN_OVER] = contract["turnover"]
                self._set_symbol(contract, row.symbol, symbols_expire)
                contract[types.DATE] = date
                contract[types.NAME] = row.symbol
                contract[types.VARIETY] = row.variety
                contract[types.SOURCE] = types.AKSHARE
                contract[types.COUNTRY] = types.CN
                contract[types.EXCHANGE] = exchange
                contract[types.GROUP] = group

                contracts.append(contract)

        logger.info("format contracts success")

        return contracts

    def _write_contracts_to_database(self, contracts):
        """write contracts to database"""

        logger.info("start write contracts to database")

        count = 0
        for contract in contracts:
            date = contract[types.DATE]
            name = contract[types.NAME]
            variety = contract[types.VARIETY]
            source = contract[types.SOURCE]
            country = contract[types.COUNTRY]
            exchange = contract[types.EXCHANGE]
            group = contract[types.GROUP]

            # check exists before insert
            db_contract = self.dbapi.contract_get_by_constraint(
                date, name, variety, source, country)
            if db_contract is not None:
                logger.info("%s %s already exists, skip", date, name)
                continue

            # insert to database
            count += 1
            logger.info("insert %s %s to database", date, name)
            self.dbapi.contract_create(date,
                                       name,
                                       variety,
                                       source,
                                       country,
                                       exchange,
                                       group,
                                       contract)

        logger.info("write %d contracts to database success", count)

        return count

    @staticmethod
    def _validate_contracts(contracts):
        """validate contracts"""

        logger.info("start validate contracts")

        # it is very dangerous for 0 close price since close price
        # is used across all the trading progress.
        for contract in contracts:
            close_price = contract[types.CLOSE]
            close_zero = close_price == 0 or pd.isnull(close_price)
            open_price = contract[types.OPEN]
            open_nan_zero = open_price != 0 and not pd.isnull(open_price)
            high_price = contract[types.HIGH]
            high_nan_zero = high_price != 0 and not pd.isnull(high_price)
            low_price = contract[types.LOW]
            low_nan_zero = low_price != 0 and not pd.isnull(low_price)

            if close_zero and (
                    open_nan_zero or high_nan_zero or low_nan_zero):
                raise exception.DataPriceInvalidTypeError

            if pd.isnull(close_price):
                raise exception.DataPriceInvalidTypeError

            # expire is also very important since we use it for rolling
            # contracts
            if types.EXPIRE not in contract:
                raise exception.DataInvalidExpireError

            if contract[types.EXPIRE] is None:
                raise exception.DataInvalidExpireError

        logger.info("validate contracts success")

    def _set_symbol(self, contract, symbol, symbols_expire):
        """set symbol"""
        if symbol in symbols_expire:
            contract[types.EXPIRE] = symbols_expire[symbol]
            return

        # black magic from the exchange, they use upper or lower
        # case chars, the little greenturtle sucks.
        lower = symbol.lower()
        if lower in symbols_expire:
            contract[types.EXPIRE] = symbols_expire[lower]
            return

        # sucks again.
        upper = symbol.upper()
        if upper in symbols_expire:
            contract[types.EXPIRE] = symbols_expire[upper]
            return

        msg = f"failed get expire for {symbol} from online, try db"
        logger.warning(msg)
        db_contracts = self.dbapi.contract_get_all_by_name_source_country(
            symbol, self.conf.source, self.conf.country)

        for db_contract in db_contracts:
            if db_contract.expire is not None:
                contract[types.EXPIRE] = db_contract.expire
                return

        msg = f"failed to get expire for {symbol} from db, raise exception"
        logger.error(msg)
        raise exception.DataInvalidExpireError

    def synchronize_delta_continuous_contracts(self):
        """synchronize delta continuous contract."""
        if not (
                (self.conf.country == types.CN) and
                (self.conf.source == types.AKSHARE)
        ):
            raise NotImplementedError

        for group in varieties.CN_VARIETIES.values():
            for variety in group:
                c = continuous_contract.DeltaContinuousContract(
                    variety, self.conf.source, self.conf.country, self.dbapi)
                c.generate()
