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

"""Process the data downloaded from binance and combine to single file."""

from datetime import datetime
import os
import pandas as pd

from greenturtle.util import time_util


# columns of the file.
cols = [
    # open time is the Greenwich Mean Time, which is similiar to UTC
    "open_time",
    "open",
    "high",
    "low",
    "close",
    "volume",  # number of the tokens.
    "close_time",
    "quote_asset_volume",  # number of the USDT tokens.
    "number_of_trades",  # number of trades
    # You may refer https://dev.binance.vision/t/relationship-between-different
    # -types-of-volume/19499/2 for more details about the columns meaning.
    # taker_buy_base_asset_volume = maker_sell_base_asset_volume
    # taker_sell_base_asset_volume = maker_buy_base_asset_volume
    # volume = taker_buy_base_asset_volume + taker_sell_base_asset_volume
    # volume = maker_sell_base_asset_volume + maker_buy_base_asset_volume
    "taker_buy_base_asset_volume",
    "taker_buy_quote_asset_volume",
    "ignore",
]


def load_data_from_files(directory):
    """
    load_data_from_files load the data from different files and combine it
    to a single csv file with sorting by opening time.
    """
    df = pd.DataFrame()
    files = os.listdir(directory)
    for file in files:
        if not file.endswith(".csv"):
            continue

        path_to_file = os.path.join(directory, file)
        tmp_df = pd.read_csv(
            path_to_file,
            index_col="open_time",  # use open time as the index.
            names=cols,
            header=None)
        df = pd.concat([df, tmp_df])

    df = df.sort_index(ascending=True)

    # convert the time format from unix timestamp to %Y-%m-%d %H:%M:%S.
    df.index = df.index.map(
        lambda x: datetime.utcfromtimestamp(
            x / 1000).strftime(time_util.DEFAULT_FORMAT),
    )
    return df


if __name__ == "__main__":

    base_dir = os.path.dirname(os.path.abspath(__file__))

    # input file path.
    BTC_1m_dir = os.path.join(base_dir, "spot/monthly/klines/BTCUSDT/1m")
    ETH_1m_dir = os.path.join(base_dir, "spot/monthly/klines/ETHUSDT/1m")
    BNBB_1m_dir = os.path.join(base_dir, "spot/monthly/klines/BNBBUSD/1m")

    BTC_1h_dir = os.path.join(base_dir, "spot/monthly/klines/BTCUSDT/1h")
    ETH_1h_dir = os.path.join(base_dir, "spot/monthly/klines/ETHUSDT/1h")
    BNBB_1h_dir = os.path.join(base_dir, "spot/monthly/klines/BNBBUSD/1h")

    BTC_1d_dir = os.path.join(base_dir, "spot/monthly/klines/BTCUSDT/1d")
    ETH_1d_dir = os.path.join(base_dir, "spot/monthly/klines/ETHUSDT/1d")
    BNBB_1d_dir = os.path.join(base_dir, "spot/monthly/klines/BNBBUSD/1d")

    # output file path.
    output_dir = os.path.join(base_dir, "output")
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    BTC_1m_csv = os.path.join(output_dir, "btc_1m.csv")
    ETH_1m_csv = os.path.join(output_dir, "eth_1m.csv")
    BNBB_1m_csv = os.path.join(output_dir, "bnbb_1m.csv")

    BTC_1h_csv = os.path.join(output_dir, "btc_1h.csv")
    ETH_1h_csv = os.path.join(output_dir, "eth_1h.csv")
    BNBB_1h_csv = os.path.join(output_dir, "bnbb_1h.csv")

    BTC_1d_csv = os.path.join(output_dir, "btc_1d.csv")
    ETH_1d_csv = os.path.join(output_dir, "eth_1d.csv")
    BNBB_1d_csv = os.path.join(output_dir, "bnbb_1d.csv")

    # Load the 1m BTC data from files and merge it to single csv file.
    data = load_data_from_files(BTC_1m_dir)
    data.to_csv(BTC_1m_csv)

    # Load the 1m ETH data from files and merge it to single csv file.
    data = load_data_from_files(ETH_1m_dir)
    data.to_csv(ETH_1m_csv)

    # Load the 1m BNBB data from files and merge it to single csv file.
    data = load_data_from_files(BNBB_1m_dir)
    data.to_csv(BNBB_1m_csv)

    # Load the 1h BTC data from files and merge it to single csv file.
    data = load_data_from_files(BTC_1h_dir)
    data.to_csv(BTC_1h_csv)

    # Load the 1h ETH data from files and merge it to single csv file.
    data = load_data_from_files(ETH_1h_dir)
    data.to_csv(ETH_1h_csv)

    # Load the 1h BNBB data from files and merge it to single csv file.
    data = load_data_from_files(BNBB_1h_dir)
    data.to_csv(BNBB_1h_csv)

    # Load the 1d BTC data from files and merge it to single csv file.
    data = load_data_from_files(BTC_1d_dir)
    data.to_csv(BTC_1d_csv)

    # Load the 1m ETH data from files and merge it to single csv file.
    data = load_data_from_files(ETH_1d_dir)
    data.to_csv(ETH_1d_csv)

    # Load the 1m BNBB data from files and merge it to single csv file.
    data = load_data_from_files(BNBB_1d_dir)
    data.to_csv(BNBB_1d_csv)
