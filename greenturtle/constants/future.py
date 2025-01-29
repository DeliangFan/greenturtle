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

"""some constants for future"""

YAHOO_CODE = "yahoo_code"
CONTRACT_UNIT = "contract_unit"
DESCRIPTION = "description"
MARGIN_REQUIREMENT_RATIO = "margin_requirement_ratio"

# Some data is copy from
# https://www.schwab.com.sg/investment-products/us-futures-market
AGRICULTURE = {
    "CT": {
        YAHOO_CODE: "CT=F",
        CONTRACT_UNIT: 500,
        MARGIN_REQUIREMENT_RATIO: 0.1,
        DESCRIPTION: "Cotton",
    },  # 棉花
    "ZC": {
        YAHOO_CODE: "ZC=F",
        CONTRACT_UNIT: 50,
        MARGIN_REQUIREMENT_RATIO: 0.1,
        DESCRIPTION: "Corn",
    },  # 玉米
    "ZS": {
        YAHOO_CODE: "ZS=F",
        CONTRACT_UNIT: 50,
        MARGIN_REQUIREMENT_RATIO: 0.1,
        DESCRIPTION: "Soybean",
    },  # 大豆
    "ZW": {
        YAHOO_CODE: "ZW=F",
        CONTRACT_UNIT: 50,
        MARGIN_REQUIREMENT_RATIO: 0.1,
        DESCRIPTION: "Wheat",
    },  # 小麦
    "ZM": {
        YAHOO_CODE: "ZM=F",
        CONTRACT_UNIT: 100,
        MARGIN_REQUIREMENT_RATIO: 0.1,
        DESCRIPTION: "Soybean Meal",
    },  # 豆粕
    "ZL": {
        YAHOO_CODE: "ZL=F",
        CONTRACT_UNIT: 600,
        MARGIN_REQUIREMENT_RATIO: 0.1,
        DESCRIPTION: "Soybean Oil",
    },
    "LE": {
        YAHOO_CODE: "LE=F",
        CONTRACT_UNIT: 400,
        MARGIN_REQUIREMENT_RATIO: 0.1,
        DESCRIPTION: "Live Cattle",
    },  # 活牛
    "ZR": {  # seems problem with the yahoo finance data
        YAHOO_CODE: "ZR=F",
        CONTRACT_UNIT: 2000,
        MARGIN_REQUIREMENT_RATIO: 0.1,
        DESCRIPTION: "Rough Rice",
    },  # 稻谷
    "DC": {
        YAHOO_CODE: "DC=F",
        CONTRACT_UNIT: 2000,
        MARGIN_REQUIREMENT_RATIO: 0.1,
        DESCRIPTION: "Milk",
    },
    "HE": {
        YAHOO_CODE: "HE=F",
        CONTRACT_UNIT: 400,
        MARGIN_REQUIREMENT_RATIO: 0.1,
        DESCRIPTION: "Lean Hog",
    },  # 瘦肉
    "ZO": {
        YAHOO_CODE: "ZO=F",
        CONTRACT_UNIT: 50,
        MARGIN_REQUIREMENT_RATIO: 0.1,
        DESCRIPTION: "Oats",
    },  # 燕麦
}

SOFTS = {
    "CC": {
        YAHOO_CODE: "CC=F",
        CONTRACT_UNIT: 10,
        MARGIN_REQUIREMENT_RATIO: 0.1,
        DESCRIPTION: "Cocoa ICE",
    },
    "SB": {
        YAHOO_CODE: "SB=F",
        CONTRACT_UNIT: 1120,
        MARGIN_REQUIREMENT_RATIO: 0.1,
        DESCRIPTION: "Sugar",
    },
    "KC": {
        YAHOO_CODE: "KC=F",
        CONTRACT_UNIT: 375,
        MARGIN_REQUIREMENT_RATIO: 0.1,
        DESCRIPTION: "Coffee",
    },
}

METALS = {
    "GC": {
        YAHOO_CODE: "GC=F",
        CONTRACT_UNIT: 100,
        MARGIN_REQUIREMENT_RATIO: 0.1,
        DESCRIPTION: "Gold",
    },
    "SI": {
        YAHOO_CODE: "SI=F",
        CONTRACT_UNIT: 5000,
        MARGIN_REQUIREMENT_RATIO: 0.1,
        DESCRIPTION: "Silver",
    },
    "HG": {
        YAHOO_CODE: "HG=F",
        CONTRACT_UNIT: 25000,
        MARGIN_REQUIREMENT_RATIO: 0.1,
        DESCRIPTION: "Copper",
    },
    "PL": {
        YAHOO_CODE: "PL=F",
        CONTRACT_UNIT: 50,
        MARGIN_REQUIREMENT_RATIO: 0.1,
        DESCRIPTION: "Platinum",
    },  # 铂
    "PA": {
        YAHOO_CODE: "PA=F",
        CONTRACT_UNIT: 100,
        MARGIN_REQUIREMENT_RATIO: 0.1,
        DESCRIPTION: "Palladium",
    },  # 钯
}

ENERGY = {
    "CL": {
        YAHOO_CODE: "CL=F",
        CONTRACT_UNIT: 1000,
        MARGIN_REQUIREMENT_RATIO: 0.1,
        DESCRIPTION: "Crude Oil",
    },
    "NG": {
        YAHOO_CODE: "NG=F",
        CONTRACT_UNIT: 10000,
        MARGIN_REQUIREMENT_RATIO: 0.1,
        DESCRIPTION: "Natural Gas",
    },
    "HO": {
        YAHOO_CODE: "HO=F",
        CONTRACT_UNIT: 42000,
        MARGIN_REQUIREMENT_RATIO: 0.1,
        DESCRIPTION: "Heating Oil",
    },
    "RB": {
        YAHOO_CODE: "RB=F",
        CONTRACT_UNIT: 42000,
        MARGIN_REQUIREMENT_RATIO: 0.1,
        DESCRIPTION: "RBOB Gasoline",
    },  # 氧化混調型精制汽油
}

CRYPTO = {
    "BTC": {
        YAHOO_CODE: "BTC=F",
        CONTRACT_UNIT: 5,
        MARGIN_REQUIREMENT_RATIO: 0.25,
        DESCRIPTION: "Bitcoin",
    },
    "ETH": {
        YAHOO_CODE: "ETH=F",
        CONTRACT_UNIT: 50,
        MARGIN_REQUIREMENT_RATIO: 0.25,
        DESCRIPTION: "Ether",
    },
}

CURRENCY = {
    "6B": {
        YAHOO_CODE: "6B=F",
        CONTRACT_UNIT: 62500,
        MARGIN_REQUIREMENT_RATIO: 0.05,
        DESCRIPTION: "British Pound Futures",
    },
    "6J": {
        YAHOO_CODE: "6J=F",
        CONTRACT_UNIT: 12500000,
        MARGIN_REQUIREMENT_RATIO: 0.05,
        DESCRIPTION: "Japanese Yen",
    },
    "DX": {
        YAHOO_CODE: "DX=F",
        CONTRACT_UNIT: 1000,
        MARGIN_REQUIREMENT_RATIO: 0.05,
        DESCRIPTION: "US Dollar",
    },
    "6E": {
        YAHOO_CODE: "6E=F",
        CONTRACT_UNIT: 125000,
        MARGIN_REQUIREMENT_RATIO: 0.05,
        DESCRIPTION: "Euro FX",
    },
}

STOCK_INDICES = {
    "ES": {
        YAHOO_CODE: "ES=F",
        CONTRACT_UNIT: 50,
        MARGIN_REQUIREMENT_RATIO: 0.1,
        DESCRIPTION: "E-Mini S&P 500",
    },
    "NQ": {
        YAHOO_CODE: "NQ=F",
        CONTRACT_UNIT: 20,
        MARGIN_REQUIREMENT_RATIO: 0.1,
        DESCRIPTION: "E-mini Nasdaq",
    },
    "YM": {
        YAHOO_CODE: "YM=F",
        CONTRACT_UNIT: 5,
        MARGIN_REQUIREMENT_RATIO: 0.1,
        DESCRIPTION: "Mini Dow Jones Indus",
    },
    "NKD": {
        YAHOO_CODE: "NKD=F",
        CONTRACT_UNIT: 5,
        MARGIN_REQUIREMENT_RATIO: 0.1,
        DESCRIPTION: "Nikkei/USD Futures",
    },
}

INTEREST_RATES = {
    "ZB": {
        YAHOO_CODE: "ZB=F",
        CONTRACT_UNIT: 1000,
        MARGIN_REQUIREMENT_RATIO: 0.8,
        DESCRIPTION: "U.S. Treasury Bond Futures",
    },
    "ZN": {
        YAHOO_CODE: "ZN=F",
        CONTRACT_UNIT: 1000,
        MARGIN_REQUIREMENT_RATIO: 0.6,
        DESCRIPTION: "10-Year T-Note Futures",
    },
    "ZT": {
        YAHOO_CODE: "ZT=F",
        CONTRACT_UNIT: 2000,
        MARGIN_REQUIREMENT_RATIO: 0.4,
        DESCRIPTION: "U.S. 2-Year Note",
    },
}

FUTURE = {
    "agriculture": AGRICULTURE,
    "soft": SOFTS,
    "metal": METALS,
    "energy": ENERGY,
    "crypto": CRYPTO,
    "currency": CURRENCY,
    "stock_indices": STOCK_INDICES,
    "interest_rates": INTEREST_RATES,
}
