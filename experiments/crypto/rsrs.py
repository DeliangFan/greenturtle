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

"""Experiment to benchmark the RSRS performance on cryptocurrencies."""

import backtrader as bt
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression

from greenturtle.simulator.backtrader import simulator
from greenturtle.stragety.backtrader import rsrs
from greenturtle.util.logging import logging
from experiments.crypto import common


logger = logging.get_logger()

# pylint: disable=R0801
DATA_NAME = "../../download/crypto/csv/btc_1d.csv"
CRYPTO_NAME = "btc"


def get_rsrs_series(period=18):
    """get rsrs panda series."""

    df = pd.read_csv(DATA_NAME)
    high = df["high"].to_numpy()
    low = df["low"].to_numpy()

    beta_items = []
    # compute the rsrs(beta) value with linear regression.
    for i in range(period, len(high)):
        x = high[i - period:i]
        y = low[i - period:i]
        lr = LinearRegression()
        lr.fit(x.reshape(-1, 1), y)
        beta_items.append(lr.coef_[0])

    series = pd.Series(beta_items)
    return series


def show_rsrs_distribution(series, plot=True):
    """describe and show the rsrs series."""

    describe = series.describe()
    logger.info("\n%s", describe)

    # plot
    if plot:
        series.plot.hist(
            bins=50,
            title="rsrs distribution",
            xlabel="beta",
            ylabel="count")
        plt.show()


# pylint: disable=R0801
if __name__ == '__main__':

    rsrs_series = get_rsrs_series(18)
    show_rsrs_distribution(rsrs_series, plot=False)

    data = common.get_crypto_data_from_csv_file(
        CRYPTO_NAME,
        DATA_NAME,
        bt.TimeFrame.Days)
    datas = [(CRYPTO_NAME, data)]

    lower = rsrs_series.mean() - 1 * rsrs_series.std()
    upper = rsrs_series.mean() + 1.3 * rsrs_series.std()
    simulator.do_simulate(datas, rsrs.RSRSStrategy, lower=lower, upper=upper)
