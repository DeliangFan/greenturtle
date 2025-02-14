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

"""future constants for varieties."""

from greenturtle.constants.future import types


# Some data is copy from
# https://www.schwab.com.sg/investment-products/us-futures-market
US_AGRICULTURE = {
    "CT": {
        types.YAHOO_CODE: "CT=F",
        types.MULTIPLIER: 500,
        types.AUTO_MARGIN: 50,
        types.DESCRIPTION: "Cotton",
    },  # 棉花
    "ZC": {
        types.YAHOO_CODE: "ZC=F",
        types.MULTIPLIER: 50,
        types.AUTO_MARGIN: 5,
        types.DESCRIPTION: "Corn",
    },  # 玉米
    "ZS": {
        types.YAHOO_CODE: "ZS=F",
        types.MULTIPLIER: 50,
        types.AUTO_MARGIN: 5,
        types.DESCRIPTION: "Soybean",
    },  # 大豆
    "ZW": {
        types.YAHOO_CODE: "ZW=F",
        types.MULTIPLIER: 50,
        types.AUTO_MARGIN: 5,
        types.DESCRIPTION: "Wheat",
    },  # 小麦
    "ZM": {
        types.YAHOO_CODE: "ZM=F",
        types.MULTIPLIER: 100,
        types.AUTO_MARGIN: 10,
        types.DESCRIPTION: "Soybean Meal",
    },  # 豆粕
    "ZL": {
        types.YAHOO_CODE: "ZL=F",
        types.MULTIPLIER: 600,
        types.AUTO_MARGIN: 60,
        types.DESCRIPTION: "Soybean Oil",
    },
    "LE": {
        types.YAHOO_CODE: "LE=F",
        types.MULTIPLIER: 400,
        types.AUTO_MARGIN: 40,
        types.DESCRIPTION: "Live Cattle",
    },  # 活牛
    "LC": {
        types.MULTIPLIER: 400,
        types.AUTO_MARGIN: 40,
        types.DESCRIPTION: "Live Cattle",
    },  # 活牛, same as LE
    "DC": {
        types.YAHOO_CODE: "DC=F",
        types.MULTIPLIER: 2000,
        types.AUTO_MARGIN: 200,
        types.DESCRIPTION: "Milk",
    },
    "DA": {
        types.MULTIPLIER: 2000,
        types.AUTO_MARGIN: 200,
        types.DESCRIPTION: "Milk",
    },
    "HE": {
        types.YAHOO_CODE: "HE=F",
        types.MULTIPLIER: 400,
        types.AUTO_MARGIN: 40,
        types.DESCRIPTION: "Lean Hog",
    },  # 瘦肉
    "LH": {
        types.MULTIPLIER: 400,
        types.AUTO_MARGIN: 40,
        types.DESCRIPTION: "Lean Hog",
    },  # 瘦肉, same as HE
    "ZO": {
        types.YAHOO_CODE: "ZO=F",
        types.MULTIPLIER: 50,
        types.AUTO_MARGIN: 5,
        types.DESCRIPTION: "Oats",
    },  # 燕麦
}

US_SOFTS = {
    "CC": {
        types.YAHOO_CODE: "CC=F",
        types.MULTIPLIER: 10,
        types.AUTO_MARGIN: 1,
        types.DESCRIPTION: "Cocoa ICE",
    },
    "SB": {
        types.YAHOO_CODE: "SB=F",
        types.MULTIPLIER: 1120,
        types.AUTO_MARGIN: 112,
        types.DESCRIPTION: "Sugar",
    },
    "KC": {
        types.YAHOO_CODE: "KC=F",
        types.MULTIPLIER: 375,
        types.AUTO_MARGIN: 38,
        types.DESCRIPTION: "Coffee",
    },
    "OJ": {
        types.YAHOO_CODE: "OJ=F",
        types.MULTIPLIER: 150,
        types.AUTO_MARGIN: 15,
        types.DESCRIPTION: "ICE Orange Juice",
    }
}

US_METALS = {
    "GC": {
        types.YAHOO_CODE: "GC=F",
        types.MULTIPLIER: 100,
        types.AUTO_MARGIN: 10,
        types.DESCRIPTION: "Gold",
    },
    "SI": {
        types.YAHOO_CODE: "SI=F",
        types.MULTIPLIER: 5000,
        types.AUTO_MARGIN: 500,
        types.DESCRIPTION: "Silver",
    },
    "HG": {
        types.YAHOO_CODE: "HG=F",
        types.MULTIPLIER: 25000,
        types.AUTO_MARGIN: 2500,
        types.DESCRIPTION: "Copper",
    },
    "PL": {
        types.YAHOO_CODE: "PL=F",
        types.MULTIPLIER: 50,
        types.AUTO_MARGIN: 5,
        types.DESCRIPTION: "Platinum",
    },  # 铂
    "PA": {
        types.YAHOO_CODE: "PA=F",
        types.MULTIPLIER: 100,
        types.AUTO_MARGIN: 10,
        types.DESCRIPTION: "Palladium",
    },  # 钯
}

US_ENERGY = {
    "CL": {
        types.YAHOO_CODE: "CL=F",
        types.MULTIPLIER: 1000,
        types.AUTO_MARGIN: 100,
        types.DESCRIPTION: "Crude Oil",
    },
    "NG": {
        types.YAHOO_CODE: "NG=F",
        types.MULTIPLIER: 10000,
        types.AUTO_MARGIN: 1000,
        types.DESCRIPTION: "Natural Gas",
    },
    "HO": {
        types.YAHOO_CODE: "HO=F",
        types.MULTIPLIER: 42000,
        types.AUTO_MARGIN: 4200,
        types.DESCRIPTION: "Heating Oil",
    },
    "RB": {
        types.YAHOO_CODE: "RB=F",
        types.MULTIPLIER: 42000,
        types.AUTO_MARGIN: 4200,
        types.DESCRIPTION: "RBOB Gasoline",
    },  # 氧化混調型精制汽油
}

US_CRYPTO = {
    "BTC": {
        types.YAHOO_CODE: "BTC=F",
        types.MULTIPLIER: 5,
        types.AUTO_MARGIN: 1,
        types.DESCRIPTION: "Bitcoin",
    },
    "ETH": {
        types.YAHOO_CODE: "ETH=F",
        types.MULTIPLIER: 50,
        types.AUTO_MARGIN: 25,
        types.DESCRIPTION: "Ether",
    },
}

US_CURRENCY = {
    "6B": {
        types.YAHOO_CODE: "6B=F",
        types.MULTIPLIER: 62500,
        types.AUTO_MARGIN: 2000,
        types.DESCRIPTION: "British Pound Futures",
    },
    "6J": {
        types.YAHOO_CODE: "6J=F",
        types.MULTIPLIER: 12500000,
        types.AUTO_MARGIN: 600000,
        types.DESCRIPTION: "Japanese Yen",
    },
    "BP": {
        types.MULTIPLIER: 62500,
        types.AUTO_MARGIN: 2000,
        types.DESCRIPTION: "British Pound Futures",
    },
    "JY": {
        types.MULTIPLIER: 12500000,
        types.AUTO_MARGIN: 600000,
        types.DESCRIPTION: "Japanese Yen",
    },
    "DX": {
        types.YAHOO_CODE: "DX=F",
        types.MULTIPLIER: 1000,
        types.AUTO_MARGIN: 25,
        types.DESCRIPTION: "US Dollar",
    },
    "6E": {
        types.YAHOO_CODE: "6E=F",
        types.MULTIPLIER: 125000,
        types.AUTO_MARGIN: 3000,
        types.DESCRIPTION: "Euro FX",
    },
    "6A": {
        types.YAHOO_CODE: "6A=F",
        types.MULTIPLIER: 100000,
        types.AUTO_MARGIN: 3000,
        types.DESCRIPTION: "Australian Dollar",
    },
    "AD": {
        types.MULTIPLIER: 100000,
        types.AUTO_MARGIN: 3000,
        types.DESCRIPTION: "Australian Dollar",
    },
    "6C": {
        types.YAHOO_CODE: "6C=F",
        types.MULTIPLIER: 100000,
        types.AUTO_MARGIN: 3000,
        types.DESCRIPTION: "Canada Dollar",
    },
    "CD": {
        types.MULTIPLIER: 100000,
        types.AUTO_MARGIN: 3000,
        types.DESCRIPTION: "Canada Dollar",
    },
    "6S": {
        types.YAHOO_CODE: "6S=F",
        types.MULTIPLIER: 125000,
        types.AUTO_MARGIN: 4000,
        types.DESCRIPTION: "Swiss France",
    },
    "SF": {
        types.MULTIPLIER: 125000,
        types.AUTO_MARGIN: 4000,
        types.DESCRIPTION: "Swiss France",
    },
    "6N": {
        types.YAHOO_CODE: "6N=F",
        types.MULTIPLIER: 100000,
        types.AUTO_MARGIN: 3000,
        types.DESCRIPTION: "NewZealand Dollar",
    },
    "NE": {
        types.MULTIPLIER: 100000,
        types.AUTO_MARGIN: 3000,
        types.DESCRIPTION: "NewZealand Dollar",
    },
    "RP": {
        types.YAHOO_CODE: "RP=F",
        types.MULTIPLIER: 125000,
        types.AUTO_MARGIN: 4000,
        types.DESCRIPTION: "Euro/British Pound",
    },
    "RY": {
        types.YAHOO_CODE: "RY=F",
        types.MULTIPLIER: 1250,
        types.AUTO_MARGIN: 40,
        types.DESCRIPTION: "Euro/Japanese Yen",
    },
}

US_STOCK_INDICES = {
    "ES": {
        types.YAHOO_CODE: "ES=F",
        types.MULTIPLIER: 50,
        types.AUTO_MARGIN: 5,
        types.DESCRIPTION: "E-Mini S&P 500",
    },
    "NQ": {
        types.YAHOO_CODE: "NQ=F",
        types.MULTIPLIER: 20,
        types.AUTO_MARGIN: 2,
        types.DESCRIPTION: "E-mini Nasdaq",
    },
    "YM": {
        types.YAHOO_CODE: "YM=F",
        types.MULTIPLIER: 5,
        types.AUTO_MARGIN: 0.5,
        types.DESCRIPTION: "Mini Dow Jones Indus",
    },
    "NKD": {
        types.YAHOO_CODE: "NKD=F",
        types.MULTIPLIER: 5,
        types.AUTO_MARGIN: 0.5,
        types.DESCRIPTION: "Nikkei/USD Futures",
    },
}

US_INTEREST_RATES = {
    "ZB": {
        types.YAHOO_CODE: "ZB=F",
        types.MULTIPLIER: 1000,
        types.AUTO_MARGIN: 50,
        types.DESCRIPTION: "U.S. Treasury Bond Futures",
    },
    "ZN": {
        types.YAHOO_CODE: "ZN=F",
        types.MULTIPLIER: 1000,
        types.AUTO_MARGIN: 30,
        types.DESCRIPTION: "10-Year T-Note Futures",
    },
    "ZF": {
        types.YAHOO_CODE: "ZF=F",
        types.MULTIPLIER: 1000,
        types.AUTO_MARGIN: 25,
        types.DESCRIPTION: "10-Year T-Note Futures",
    },
    "ZT": {
        types.YAHOO_CODE: "ZT=F",
        types.MULTIPLIER: 2000,
        types.AUTO_MARGIN: 25,
        types.DESCRIPTION: "U.S. 2-Year Note",
    },
}

US_VARIETIES = {
    "agriculture": US_AGRICULTURE,
    "soft": US_SOFTS,
    "metal": US_METALS,
    "energy": US_ENERGY,
    "crypto": US_CRYPTO,
    "currency": US_CURRENCY,
    "stock_indices": US_STOCK_INDICES,
    "interest_rates": US_INTEREST_RATES,
}

DEFAULT_RISK_FACTOR = 0.002
DEFAULT_GROUP_RISK_FACTORS = {
    "agriculture": 0.01,
    "soft": 0.01,
    "metal": 0.01,
    "energy": 0.01,
    "crypto": 0.01,
    "currency": 0.01,
    "stock_indices": 0.01,
    "interest_rates": 0.01,
}
