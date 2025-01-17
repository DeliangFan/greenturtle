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

AGRICULTURE = {
    "CT": {YAHOO_CODE: "CT=F", "description": "Cotton"},  # 棉花
    "ZC": {YAHOO_CODE: "ZC=F", "description": "Corn"},  # 玉米
    "ZS": {YAHOO_CODE: "ZS=F", "description": "Soybean"},  # 大豆
    "ZW": {YAHOO_CODE: "ZW=F", "description": "Wheat"},  # 小麦
    "ZM": {YAHOO_CODE: "ZM=F", "description": "Soybean Meal"},  # 豆粕
    "ZL": {YAHOO_CODE: "ZL=F", "description": "Soybean Oil"},
    "LE": {YAHOO_CODE: "LE=F", "description": "Live Cattle"},  # 活牛
    "ZR": {YAHOO_CODE: "ZR=F", "description": "Rough Rice"},  # 稻谷
    "DC": {YAHOO_CODE: "DC=F", "description": "Milk"},
    "HE": {YAHOO_CODE: "HE=F", "description": "Lean Hog"},  # 瘦肉
    "ZO": {YAHOO_CODE: "ZO=F", "description": "Oats"},  # 燕麦
}

SOFTS = {
    "CC": {YAHOO_CODE: "CC=F", "description": "Cocoa ICE"},
    "SB": {YAHOO_CODE: "SB=F", "description": "Sugar"},
    "KC": {YAHOO_CODE: "KC=F", "description": "Coffee"},
}

METALS = {
    "GC": {YAHOO_CODE: "GC=F", "description": "Gold"},
    "SI": {YAHOO_CODE: "SI=F", "description": "Silver"},
    "HG": {YAHOO_CODE: "HG=F", "description": "Copper"},
    "PL": {YAHOO_CODE: "PL=F", "description": "Platinum"},  # 铂
    "PA": {YAHOO_CODE: "PA=F", "description": "Palladium"},  # 钯
}

ENERGY = {
    "CL": {YAHOO_CODE: "CL=F", "description": "Crude Oil"},
    "NG": {YAHOO_CODE: "NG=F", "description": "Natural Gas"},
    "HO": {YAHOO_CODE: "HO=F", "description": "Heating Oil"},
    "RB": {YAHOO_CODE: "RB=F", "description": "RBOB Gasoline"},  # 氧化混調型精制汽油
}

CRYPTO = {
    "BTC": {YAHOO_CODE: "BTC=F", "description": "Bitcoin"},
    "ETH": {YAHOO_CODE: "ETH=F", "description": "Ether"},
}

CURRENCY = {
    "6B": {YAHOO_CODE: "6B=F", "description": "British Pound Futures"},
    "6J": {YAHOO_CODE: "6J=F", "description": "Japanese Yen"},
    "DX": {YAHOO_CODE: "DX=F", "description": "US Dollar"},
    "6E": {YAHOO_CODE: "6E=F", "description": "Euro FX"},
}

STOCK_INDICES = {
    "ES": {YAHOO_CODE: "ES=F", "description": "E-Mini S&P 500"},
    "NQ": {YAHOO_CODE: "NQ=F", "description": "E-mini Nasdaq"},
    "YM": {YAHOO_CODE: "YM=F", "description": "Mini Dow Jones Indus"},
    "NKD": {YAHOO_CODE: "NKD=F", "description": "Nikkei/USD Futures"},
}

INTEREST_RATES = {
    "ZB": {YAHOO_CODE: "ZB=F", "description": "U.S. Treasury Bond Futures"},
    "ZN": {YAHOO_CODE: "ZN=F", "description": "10-Year T-Note Futures"},
    "ZT": {YAHOO_CODE: "ZT=F", "description": "U.S. 2-Year Note	"},
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
