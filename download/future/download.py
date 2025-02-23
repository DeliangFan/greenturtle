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


"""
scripts to download and generate the data for backtesting

For cn future markets, the data are download from.
交易所               交易所代码	合约后缀     地址
中国金融期货交易所	    CFFEX	    .CFX	    http://www.cffex.com.cn
上海期货交易所	    SHFE	    .SHF	    https://www.shfe.com.cn
上海国际能源交易中心	INE	        .INE	    https://www.ine.cn
郑州商品交易所	    CZCE	    .ZCE	    http://www.czce.com.cn
大连商品交易所	    DCE	        .DCE	    http://www.dce.com.cn
广州期货交易所	    GFEX	    .GFEX	    http://www.gfex.com.cn

For us future markets, it would better to buy data from third part provider.
"""

from greenturtle.data.download import future


DST_DIR = "./source/cn"
CN_MARKETS = {
    "CFFEX": {
        "start_year": 2011,
        "end_year": 2025,
    },
    "DCE": {
        "start_year": 2001,
        "end_year": 2025,
    },
    "INE": {
        "start_year": 2019,
        "end_year": 2025,
    },
    "CZCE": {
        # you would better not download the data ten years ago
        # since the CZCE symbol name will repeat every 10 years.
        # Fuck the CZCE, so stupid naming approach.
        "start_year": 2017,
        "end_year": 2025,
    },
    "GFEX": {
        "start_year": 2023,
        "end_year": 2025,
    },
    "SHFE": {
        "start_year": 2003,
        "end_year": 2025,
    },
}


if __name__ == "__main__":
    f = future.FullCNFutureToFileFromAKShare(
        CN_MARKETS,
        DST_DIR,
    )
    f.download()
