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

"""Experiment to benchmark the trending trading performance on us futures."""

import datetime

import pandas as pd

from greenturtle.analyzers import correlation
from greenturtle.constants import types
from greenturtle.constants import varieties
from greenturtle.data.datafeed import db
from greenturtle.backtesting import backtesting
from greenturtle.stragety import ema
from greenturtle.util.logging import logging
from greenturtle.util import config


logger = logging.get_logger()

SKIP_LISTS = ["PS"]


if __name__ == '__main__':

    conf = config.load_config("/etc/greenturtle/greenturtle.yaml")
    corr = correlation.Correlation()
    df = pd.DataFrame()

    start_date = datetime.datetime(2004, 1, 1)
    end_date = x = datetime.datetime(2024, 12, 31)

    for group in varieties.CN_VARIETIES.values():
        for name in group:
            if name in SKIP_LISTS:
                continue

            s = backtesting.BackTesting(varieties=varieties.CN_VARIETIES)
            s.set_default_commission_by_name(name)
            s.add_strategy(ema.EMA,
                           risk_factor=0.02,
                           varieties=varieties.CN_VARIETIES,
                           allow_short=True)

            # pylint: disable=R0801
            data = db.ContinuousContractDB(db_conf=conf.db,
                                           variety=name,
                                           source=types.AKSHARE,
                                           country=types.CN,
                                           start_date=start_date,
                                           end_date=end_date,
                                           padding=True)
            s.add_data(data, name)

            # do backtesting
            s.do_backtesting()

            corr.add_return_summary(name, s.summary.return_summary)

            # construct the result and append it to the dataframe
            row = {
                "name": [name],
                "total_return": [
                    s.summary.return_summary.total_return],
                "annual_return": [
                    s.summary.return_summary.annual_return],
                "sharpe_ratio": [
                    s.summary.sharpe_ratio_summary.sharpe_ratio],
                "leverage": [
                    s.summary.leverage_ratio_summary.leverage_ratio],
                "max_draw_down": [
                    s.summary.max_draw_down_summary.max_draw_down],
            }

            if s.summary.trade_summary is not None:
                row["trader_number"] = [
                    s.summary.trade_summary.trader_number]
                row["win_trader_number"] = [
                    s.summary.trade_summary.win_trader_number]

            new_df = pd.DataFrame(row)
            df = pd.concat([df, new_df])

    logger.info("\n%s", df.to_string())

    result = corr.compute_correlation()
    logger.info("\n%s", result.to_string())
