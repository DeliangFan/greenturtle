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
import os

import backtrader as bt
import pandas as pd

from greenturtle.analyzers import correlation
import greenturtle.constants.future as future_const
import greenturtle.data.backtrader.future as future_data
from greenturtle.simulator.backtrader import future_simulator
from greenturtle.stragety.backtrader import ema
from greenturtle.util.logging import logging


logger = logging.get_logger()
# pylint: disable=R0801
DATA_DIR = "../../download/future_us/output/main"
# NOTE(fixme) ZR data in yahoo finance looks bad
SKIP_LIST = ("ZR",)


if __name__ == '__main__':

    c = correlation.Correlation()
    df = pd.DataFrame()

    fromdate = datetime.datetime(2004, 1, 1)
    todate = x = datetime.datetime(2024, 12, 31)

    for category_name, category_value in future_const.FUTURE.items():
        category_dir = os.path.join(DATA_DIR, category_name)
        for name, future in category_value.items():
            if name in SKIP_LIST:
                continue

            s = future_simulator.FutureSimulator()
            s.set_default_commission_by_name(name)
            s.add_strategy(ema.EMA)

            # get the data
            filename = os.path.join(DATA_DIR, f"{category_name}/{name}.csv")
            data = future_data.get_feed_from_csv_file(
                name,
                filename,
                timeframe=bt.TimeFrame.Days,
                fromdate=fromdate,
                todate=todate)
            s.add_data(data, name)

            # do simulate
            s.do_simulate()

            c.add_return_summary(name, s.summary.return_summary)

            # construct the result and append it to the dataframe
            row = {
                "name": [name],
                "category": [category_name],
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

    corr = c.compute_correlation()
    logger.info("\n%s", corr.to_string())
