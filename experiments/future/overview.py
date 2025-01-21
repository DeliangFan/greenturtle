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

from greenturtle.analysis.backtrader import base
from greenturtle.stragety.backtrader import macd
from greenturtle.util.constants import constants_future
from experiments.future import common

# pylint: disable=R0801
DATA_DIR = "../../download/future_us/output"
SKIP_LIST = ("6B", "6J", "DX", "6E", "ZN", "ZT")

# pylint: disable=line-too-long
"""
FYI, the RefinedMACDStrategy works pretty good in most of the future

  name        category  total_return  annual_return  sharpe_ratio  max_draw_down  total_trade  won_ratio
0   CT     agriculture   1407.753343      11.220021      0.519794      48.504194          240   0.508333
0   ZC     agriculture   1151.903957      10.590969      0.590483      33.232457          254   0.472441
0   ZS     agriculture    632.589333       7.904948      0.552564      43.112983          260   0.523077
0   ZW     agriculture   1927.754363      12.934745      0.663958      36.787039          253   0.490119
0   ZM     agriculture   1185.465695      10.716343      0.586185      41.713770          250   0.492000
0   ZL     agriculture   1517.119845      11.769239      0.643800      40.503837          256   0.519531
0   LE     agriculture    201.587463       3.001908      0.268381      33.489413          241   0.514523
0   ZR     agriculture    538.934935       6.924404      0.317340      52.756693          248   0.467742
0   DC     agriculture    246.512037       5.071419      0.268633      44.571436          167   0.455090
0   HE     agriculture    671.827357       8.270218      0.510074      53.448335          210   0.485714
0   ZO     agriculture    776.395405       8.691374      0.393759      73.014259          228   0.447368
0   CC            soft   2647.040791      14.080154      0.391420      50.043368          247   0.497976
0   SB            soft   7474.000992      19.071688      1.014541      34.837052          241   0.514523
0   KC            soft   3702.505521      15.635273      0.742195      45.215123          266   0.500000
0   GC           metal    645.322840       8.000480      0.752894      20.152534          241   0.497925
0   SI           metal   1119.876230      10.482395      0.618908      30.277701          250   0.464000
0   HG           metal   1005.544276       9.987390      0.509049      35.762204          253   0.474308
0   PL           metal    299.240907       4.606655      0.268194      56.485109          258   0.449612
0   PA           metal    222.867331       3.341085      0.193857      75.401021          262   0.389313
0   CL          energy   9343.485822      20.564161      0.635211     239.952950          250   0.576000
0   NG          energy  18991.382351      24.154109      0.791957      49.779496          253   0.517787
0   HO          energy   3148.073709      15.293650      0.725062      42.718267          252   0.515873
0   RB          energy   1528.346405      11.988090      0.528480      52.639949          258   0.476744
0  BTC          crypto   3165.174422      63.536966      0.691347      40.602861           62   0.532258
0  ETH          crypto    505.091604      51.529868      0.880344      45.985959           36   0.555556
0   6B        currency    149.201919       1.680905      0.157034      19.905670          237   0.493671
0   6J        currency    159.699421       1.966377      0.166275      20.981541          272   0.437500
0   DX        currency    141.459048       1.421337      0.108162      15.856327          253   0.415020
0   6E        currency    173.415889       2.287076      0.216206      24.293560          249   0.417671
0   ES   stock_indices    684.587180       8.224874      0.900022      23.005237          241   0.572614
0   NQ   stock_indices   1246.474491      10.922779      0.762772      28.020449          229   0.563319
0   YM   stock_indices    578.322815       8.032560      1.011432      19.532330          216   0.550926
0  NKD   stock_indices    661.890116       9.490193      0.701540      36.361288          204   0.485294
0   ZB  interest_rates    231.234599       3.523058      0.475738      20.697821          242   0.487603
0   ZN  interest_rates    149.195598       1.667936      0.184103       8.873992          225   0.471111
0   ZT  interest_rates     71.313185      -1.373349     -1.420105      30.490390          264   0.178030
"""  # noqa: E501


if __name__ == '__main__':

    df = pd.DataFrame()
    todate = x = datetime.datetime(2024, 12, 31)
    for category_name, category_value in constants_future.FUTURE.items():
        category_dir = os.path.join(DATA_DIR, category_name)
        for name, future in category_value.items():
            if name in SKIP_LIST:
                continue
            # get the data
            filename = os.path.join(DATA_DIR, f"{category_name}/{name}.csv")
            data = common.get_us_future_data_from_csv_file(
                name,
                filename,
                bt.TimeFrame.Days,
                todate=todate)
            datas = [(name, data)]

            # do analysis
            ana = base.do_analysis(datas, macd.RefinedMACDStrategy, plot=False)

            # construct the result and append it to the dataframe
            row = {
                "name": [name],
                "category": [category_name],
                "total_return": [ana.total_return],
                "annual_return": [ana.annual_return],
                "sharpe_ratio": [ana.sharpe_ratio],
                "max_draw_down": [ana.max_draw_down],
                "total_trade": [ana.total],
                "won_ratio": [ana.won_ratio],
            }

            new_df = pd.DataFrame(row)
            df = pd.concat([df, new_df])

    print(df.to_string())
