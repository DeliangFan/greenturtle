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
CONTRACT_NAME = "contract_name"
MULTIPLIER = "multiplier"
DESCRIPTION = "description"
MARGIN_RATIO = "margin_ratio"

# Some data is copy from
# https://www.schwab.com.sg/investment-products/us-futures-market
AGRICULTURE = {
    "CT": {
        YAHOO_CODE: "CT=F",
        MULTIPLIER: 500,
        MARGIN_RATIO: 0.1,
        DESCRIPTION: "Cotton",
    },  # 棉花
    "ZC": {
        YAHOO_CODE: "ZC=F",
        MULTIPLIER: 50,
        MARGIN_RATIO: 0.1,
        DESCRIPTION: "Corn",
    },  # 玉米
    "ZS": {
        YAHOO_CODE: "ZS=F",
        MULTIPLIER: 50,
        MARGIN_RATIO: 0.1,
        DESCRIPTION: "Soybean",
    },  # 大豆
    "ZW": {
        YAHOO_CODE: "ZW=F",
        MULTIPLIER: 50,
        MARGIN_RATIO: 0.1,
        DESCRIPTION: "Wheat",
    },  # 小麦
    "ZM": {
        YAHOO_CODE: "ZM=F",
        MULTIPLIER: 100,
        MARGIN_RATIO: 0.1,
        DESCRIPTION: "Soybean Meal",
    },  # 豆粕
    "ZL": {
        YAHOO_CODE: "ZL=F",
        MULTIPLIER: 600,
        MARGIN_RATIO: 0.1,
        DESCRIPTION: "Soybean Oil",
    },
    "LE": {
        YAHOO_CODE: "LE=F",
        MULTIPLIER: 400,
        MARGIN_RATIO: 0.1,
        DESCRIPTION: "Live Cattle",
    },  # 活牛
    "ZR": {  # seems problem with the yahoo finance data
        YAHOO_CODE: "ZR=F",
        MULTIPLIER: 2000,
        MARGIN_RATIO: 0.1,
        DESCRIPTION: "Rough Rice",
    },  # 稻谷
    "DC": {
        YAHOO_CODE: "DC=F",
        MULTIPLIER: 2000,
        MARGIN_RATIO: 0.1,
        DESCRIPTION: "Milk",
    },
    "HE": {
        YAHOO_CODE: "HE=F",
        MULTIPLIER: 400,
        MARGIN_RATIO: 0.1,
        DESCRIPTION: "Lean Hog",
    },  # 瘦肉
    "ZO": {
        YAHOO_CODE: "ZO=F",
        MULTIPLIER: 50,
        MARGIN_RATIO: 0.1,
        DESCRIPTION: "Oats",
    },  # 燕麦
}

SOFTS = {
    "CC": {
        YAHOO_CODE: "CC=F",
        MULTIPLIER: 10,
        MARGIN_RATIO: 0.1,
        DESCRIPTION: "Cocoa ICE",
    },
    "SB": {
        YAHOO_CODE: "SB=F",
        MULTIPLIER: 1120,
        MARGIN_RATIO: 0.1,
        DESCRIPTION: "Sugar",
    },
    "KC": {
        YAHOO_CODE: "KC=F",
        MULTIPLIER: 375,
        MARGIN_RATIO: 0.1,
        DESCRIPTION: "Coffee",
    },
}

METALS = {
    "GC": {
        YAHOO_CODE: "GC=F",
        MULTIPLIER: 100,
        MARGIN_RATIO: 0.1,
        DESCRIPTION: "Gold",
    },
    "SI": {
        YAHOO_CODE: "SI=F",
        MULTIPLIER: 5000,
        MARGIN_RATIO: 0.1,
        DESCRIPTION: "Silver",
    },
    "HG": {
        YAHOO_CODE: "HG=F",
        MULTIPLIER: 25000,
        MARGIN_RATIO: 0.1,
        DESCRIPTION: "Copper",
    },
    "PL": {
        YAHOO_CODE: "PL=F",
        MULTIPLIER: 50,
        MARGIN_RATIO: 0.1,
        DESCRIPTION: "Platinum",
    },  # 铂
    "PA": {
        YAHOO_CODE: "PA=F",
        MULTIPLIER: 100,
        MARGIN_RATIO: 0.1,
        DESCRIPTION: "Palladium",
    },  # 钯
}

ENERGY = {
    "CL": {
        YAHOO_CODE: "CL=F",
        MULTIPLIER: 1000,
        MARGIN_RATIO: 0.1,
        DESCRIPTION: "Crude Oil",
    },
    "NG": {
        YAHOO_CODE: "NG=F",
        MULTIPLIER: 10000,
        MARGIN_RATIO: 0.1,
        DESCRIPTION: "Natural Gas",
    },
    "HO": {
        YAHOO_CODE: "HO=F",
        MULTIPLIER: 42000,
        MARGIN_RATIO: 0.1,
        DESCRIPTION: "Heating Oil",
    },
    "RB": {
        YAHOO_CODE: "RB=F",
        MULTIPLIER: 42000,
        MARGIN_RATIO: 0.1,
        DESCRIPTION: "RBOB Gasoline",
    },  # 氧化混調型精制汽油
}

CRYPTO = {
    "BTC": {
        YAHOO_CODE: "BTC=F",
        MULTIPLIER: 5,
        MARGIN_RATIO: 0.25,
        DESCRIPTION: "Bitcoin",
    },
    "ETH": {
        YAHOO_CODE: "ETH=F",
        MULTIPLIER: 50,
        MARGIN_RATIO: 0.25,
        DESCRIPTION: "Ether",
    },
}

CURRENCY = {
    "6B": {
        YAHOO_CODE: "6B=F",
        MULTIPLIER: 62500,
        MARGIN_RATIO: 0.05,
        DESCRIPTION: "British Pound Futures",
    },
    "6J": {
        YAHOO_CODE: "6J=F",
        MULTIPLIER: 12500000,
        MARGIN_RATIO: 0.05,
        DESCRIPTION: "Japanese Yen",
    },
    "DX": {
        YAHOO_CODE: "DX=F",
        MULTIPLIER: 1000,
        MARGIN_RATIO: 0.05,
        DESCRIPTION: "US Dollar",
    },
    "6E": {
        YAHOO_CODE: "6E=F",
        MULTIPLIER: 125000,
        MARGIN_RATIO: 0.05,
        DESCRIPTION: "Euro FX",
    },
}

STOCK_INDICES = {
    "ES": {
        YAHOO_CODE: "ES=F",
        MULTIPLIER: 50,
        MARGIN_RATIO: 0.1,
        DESCRIPTION: "E-Mini S&P 500",
    },
    "NQ": {
        YAHOO_CODE: "NQ=F",
        MULTIPLIER: 20,
        MARGIN_RATIO: 0.1,
        DESCRIPTION: "E-mini Nasdaq",
    },
    "YM": {
        YAHOO_CODE: "YM=F",
        MULTIPLIER: 5,
        MARGIN_RATIO: 0.1,
        DESCRIPTION: "Mini Dow Jones Indus",
    },
    "NKD": {
        YAHOO_CODE: "NKD=F",
        MULTIPLIER: 5,
        MARGIN_RATIO: 0.1,
        DESCRIPTION: "Nikkei/USD Futures",
    },
}

INTEREST_RATES = {
    "ZB": {
        YAHOO_CODE: "ZB=F",
        MULTIPLIER: 1000,
        MARGIN_RATIO: 0.8,
        DESCRIPTION: "U.S. Treasury Bond Futures",
    },
    "ZN": {
        YAHOO_CODE: "ZN=F",
        MULTIPLIER: 1000,
        MARGIN_RATIO: 0.6,
        DESCRIPTION: "10-Year T-Note Futures",
    },
    "ZT": {
        YAHOO_CODE: "ZT=F",
        MULTIPLIER: 2000,
        MARGIN_RATIO: 0.4,
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

# month codes alphabets to number
MONTH_CODES_A2N = {
    "F": "01",
    "G": "02",
    "H": "03",
    "J": "04",
    "K": "05",
    "M": "06",
    "N": "07",
    "Q": "08",
    "U": "09",
    "V": "10",
    "X": "11",
    "Z": "12",
}

# month codes number to alphabets
MONTH_CODES_N2A = {
    "01": "F",
    "02": "G",
    "03": "H",
    "04": "J",
    "05": "K",
    "06": "M",
    "07": "N",
    "08": "Q",
    "09": "U",
    "10": "V",
    "11": "X",
    "12": "Z",
}
