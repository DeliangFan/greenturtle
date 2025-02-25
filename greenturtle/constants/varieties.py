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

from greenturtle.constants import types


DEFAULT_RISK_FACTOR = 0.002

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
    "metal": US_METALS,
    "energy": US_ENERGY,
    "crypto": US_CRYPTO,
    "currency": US_CURRENCY,
    "stock_indices": US_STOCK_INDICES,
    "interest_rates": US_INTEREST_RATES,
}

DEFAULT_US_GROUP_RISK_FACTORS = {
    "agriculture": 0.02,
    "metal": 0.01,
    "energy": 0.01,
    "crypto": 0.01,
    "currency": 0.01,
    "stock_indices": 0.01,
    "interest_rates": 0.01,
}

CN_AGRICULTURE = {
    "C": {
        types.MULTIPLIER: 10,
        types.AUTO_MARGIN: 1,
        types.DESCRIPTION: "玉米",
    },
    "CS": {
        types.MULTIPLIER: 10,
        types.AUTO_MARGIN: 1,
        types.DESCRIPTION: "玉米淀粉",
    },
    "A": {
        types.MULTIPLIER: 10,
        types.AUTO_MARGIN: 1,
        types.DESCRIPTION: "黄大豆1号",
    },
    "M": {
        types.MULTIPLIER: 10,
        types.AUTO_MARGIN: 1,
        types.DESCRIPTION: "豆粕",
    },
    "Y": {
        types.MULTIPLIER: 10,
        types.AUTO_MARGIN: 1,
        types.DESCRIPTION: "大豆原油",
    },
    "P": {
        types.MULTIPLIER: 10,
        types.AUTO_MARGIN: 1,
        types.DESCRIPTION: "棕榈油",
    },
    "JD": {
        types.MULTIPLIER: 5,
        types.AUTO_MARGIN: 0.5,
        types.DESCRIPTION: "鲜鸡蛋",
    },
    "RR": {
        types.MULTIPLIER: 10,
        types.AUTO_MARGIN: 1,
        types.DESCRIPTION: "粳米",
    },
    "LH": {
        types.MULTIPLIER: 16,
        types.AUTO_MARGIN: 1.6,
        types.DESCRIPTION: "生猪",
    },
    "PK": {
        types.MULTIPLIER: 5,
        types.AUTO_MARGIN: 0.5,
        types.DESCRIPTION: "花生仁",
    },
    "SR": {
        types.MULTIPLIER: 10,
        types.AUTO_MARGIN: 1,
        types.DESCRIPTION: "白砂糖（简称“白糖”）",
    },
    "CF": {
        types.MULTIPLIER: 5,
        types.AUTO_MARGIN: 0.5,
        types.DESCRIPTION: "棉花",
    },
    "RM": {
        types.MULTIPLIER: 10,
        types.AUTO_MARGIN: 1,
        types.DESCRIPTION: "菜籽粕（简称“菜粕”）",
    },
    "OI": {
        types.MULTIPLIER: 10,
        types.AUTO_MARGIN: 1,
        types.DESCRIPTION: "菜籽油（简称“菜油”）",
    },
    "AP": {
        types.MULTIPLIER: 10,
        types.AUTO_MARGIN: 1,
        types.DESCRIPTION: "鲜苹果（简称“苹果”）",
    },
    "CJ": {
        types.MULTIPLIER: 5,
        types.AUTO_MARGIN: 0.5,
        types.DESCRIPTION: "干制红枣（简称“红枣”）",
    },
}

CN_METALS = {
    "CU": {
        types.MULTIPLIER: 5,
        types.AUTO_MARGIN: 0.5,
        types.DESCRIPTION: "阴极铜",
    },
    "AL": {
        types.MULTIPLIER: 5,
        types.AUTO_MARGIN: 0.5,
        types.DESCRIPTION: "铝",
    },
    "ZN": {
        types.MULTIPLIER: 5,
        types.AUTO_MARGIN: 0.5,
        types.DESCRIPTION: "锌",
    },
    "PB": {
        types.MULTIPLIER: 5,
        types.AUTO_MARGIN: 0.5,
        types.DESCRIPTION: "铅",
    },
    "NI": {
        types.MULTIPLIER: 1,
        types.AUTO_MARGIN: 0.1,
        types.DESCRIPTION: "镍",
    },
    "SN": {
        types.MULTIPLIER: 1,
        types.AUTO_MARGIN: 0.1,
        types.DESCRIPTION: "锡",
    },
    "SI": {
        types.MULTIPLIER: 5,
        types.AUTO_MARGIN: 0.5,
        types.DESCRIPTION: "工业硅",
    },
    "AO": {
        types.MULTIPLIER: 20,
        types.AUTO_MARGIN: 2,
        types.DESCRIPTION: "氧化铝",
    },
    "LC": {
        types.MULTIPLIER: 1,
        types.AUTO_MARGIN: 0.1,
        types.DESCRIPTION: "碳酸锂",
    },
    "PS": {
        types.MULTIPLIER: 3,
        types.AUTO_MARGIN: 0.3,
        types.DESCRIPTION: "多晶硅",
    },
    "RB": {
        types.MULTIPLIER: 10,
        types.AUTO_MARGIN: 1,
        types.DESCRIPTION: "螺纹钢",
    },
    "HC": {
        types.MULTIPLIER: 10,
        types.AUTO_MARGIN: 1,
        types.DESCRIPTION: "热轧卷板",
    },
    "SS": {
        types.MULTIPLIER: 5,
        types.AUTO_MARGIN: 0.5,
        types.DESCRIPTION: "不锈钢",
    },
    "J": {
        types.MULTIPLIER: 100,
        types.AUTO_MARGIN: 10,
        types.DESCRIPTION: "冶金焦炭",
    },
    "JM": {
        types.MULTIPLIER: 60,
        types.AUTO_MARGIN: 6,
        types.DESCRIPTION: "焦煤",
    },
    "I": {
        types.MULTIPLIER: 100,
        types.AUTO_MARGIN: 10,
        types.DESCRIPTION: "铁矿石",
    },
    "SM": {
        types.MULTIPLIER: 5,
        types.AUTO_MARGIN: 0.5,
        types.DESCRIPTION: "锰硅",
    },
    "AU": {
        types.MULTIPLIER: 1000,
        types.AUTO_MARGIN: 100,
        types.DESCRIPTION: "黄金",
    },
    "AG": {
        types.MULTIPLIER: 15,
        types.AUTO_MARGIN: 1.5,
        types.DESCRIPTION: "白银",
    },
}

CN_ENERGY = {
    "LU": {
        types.MULTIPLIER: 10,
        types.AUTO_MARGIN: 1,
        types.DESCRIPTION: "低硫燃料油",
    },
    "FU": {
        types.MULTIPLIER: 10,
        types.AUTO_MARGIN: 1,
        types.DESCRIPTION: "燃料油",
    },
    "BU": {
        types.MULTIPLIER: 10,
        types.AUTO_MARGIN: 1,
        types.DESCRIPTION: "石油沥青",
    },
    "RU": {
        types.MULTIPLIER: 10,
        types.AUTO_MARGIN: 1,
        types.DESCRIPTION: "天然橡胶",
    },
    "NR": {
        types.MULTIPLIER: 10,
        types.AUTO_MARGIN: 1,
        types.DESCRIPTION: "20号胶",
    },
    "SP": {
        types.MULTIPLIER: 10,
        types.AUTO_MARGIN: 1,
        types.DESCRIPTION: "漂白硫酸盐针叶木浆",
    },
    "TA": {
        types.MULTIPLIER: 5,
        types.AUTO_MARGIN: 0.5,
        types.DESCRIPTION: "精对苯二甲酸（PTA）",
    },
    "MA": {
        types.MULTIPLIER: 10,
        types.AUTO_MARGIN: 1,
        types.DESCRIPTION: "甲醇",
    },
    "FG": {
        types.MULTIPLIER: 20,
        types.AUTO_MARGIN: 2,
        types.DESCRIPTION: "平板玻璃（简称“玻璃”）",
    },
    "UR": {
        types.MULTIPLIER: 20,
        types.AUTO_MARGIN: 2,
        types.DESCRIPTION: "尿素",
    },
    "SA": {
        types.MULTIPLIER: 20,
        types.AUTO_MARGIN: 2,
        types.DESCRIPTION: "纯碱",
    },
    "L": {
        types.MULTIPLIER: 5,
        types.AUTO_MARGIN: 0.5,
        types.DESCRIPTION: "线型低密度聚乙烯",
    },
    "V": {
        types.MULTIPLIER: 5,
        types.AUTO_MARGIN: 0.5,
        types.DESCRIPTION: "聚氯乙烯",
    },
    "PP": {
        types.MULTIPLIER: 5,
        types.AUTO_MARGIN: 0.5,
        types.DESCRIPTION: "聚丙烯",
    },
    "EG": {
        types.MULTIPLIER: 10,
        types.AUTO_MARGIN: 1,
        types.DESCRIPTION: "乙二醇",
    },
    "EB": {
        types.MULTIPLIER: 5,
        types.AUTO_MARGIN: 0.5,
        types.DESCRIPTION: "苯乙烯",
    },
    "PG": {
        types.MULTIPLIER: 20,
        types.AUTO_MARGIN: 2,
        types.DESCRIPTION: "液化石油气",
    },
    "PF": {
        types.MULTIPLIER: 5,
        types.AUTO_MARGIN: 0.5,
        types.DESCRIPTION: "涤纶短纤（简称“短纤”）",
    },
    "BR": {
        types.MULTIPLIER: 5,
        types.AUTO_MARGIN: 0.5,
        types.DESCRIPTION: "丁二烯橡胶",
    },
    "PX": {
        types.MULTIPLIER: 5,
        types.AUTO_MARGIN: 0.5,
        types.DESCRIPTION: "对二甲苯",
    },
    "SH": {
        types.MULTIPLIER: 30,
        types.AUTO_MARGIN: 3,
        types.DESCRIPTION: "烧碱",
    },
}

CN_INDICES = {
    "EC": {
        types.MULTIPLIER: 50,
        types.AUTO_MARGIN: 6,
        types.DESCRIPTION: "上海出口集装箱结算运价指数（欧洲航线）",
    },
    "IF": {
        types.MULTIPLIER: 300,
        types.AUTO_MARGIN: 30,
        types.DESCRIPTION: "沪深300指数",
    },
    "IC": {
        types.MULTIPLIER: 200,
        types.AUTO_MARGIN: 20,
        types.DESCRIPTION: "中证500指数",
    },
    "IM": {
        types.MULTIPLIER: 200,
        types.AUTO_MARGIN: 20,
        types.DESCRIPTION: "中证1000指数",
    },
    "IH": {
        types.MULTIPLIER: 300,
        types.AUTO_MARGIN: 30,
        types.DESCRIPTION: "上证50指数",
    },
    "TS": {
        types.MULTIPLIER: 20000,
        types.AUTO_MARGIN: 100,
        types.DESCRIPTION: "面值为200万元人民币、票面利率为3%的名义(2)中短期国债",
    },
    "TF": {
        types.MULTIPLIER: 10000,
        types.AUTO_MARGIN: 200,
        types.DESCRIPTION: "面值为100万元人民币、票面利率为3%的名义(5)中期国债",
    },
    "T": {
        types.MULTIPLIER: 10000,
        types.AUTO_MARGIN: 300,
        types.DESCRIPTION: "面值为100万元人民币、票面利率为3%的名义(10)长期国债",
    },
    "TL": {
        types.MULTIPLIER: 10000,
        types.AUTO_MARGIN: 500,
        types.DESCRIPTION: "面值为100万元人民币、票面利率为3%的名义(10)超长期国债",
    },
}

# For china future, these data are from
# https://www.cfachina.org/servicesupport/sspz/
# Due to the data quality and low volume, these varieties will be skipped.
# - WR(线材)
# - BC(国际铜)
# - LG(原木)
# - FB(纤维板)
# - BB(胶合板)
# - B(黄大豆2号)
# - ZC(动力煤)
# - WH(强麦)
# - RS(油菜籽)
# - RI(早籼稻)
# - PR(瓶片)
# - PM(普麦)
# - LR(晚稻)
# - JR(粳稻)
# - SC(国际原油)
# - CY(棉纱)
# - SF(硅铁)
CN_VARIETIES = {
    "agriculture": CN_AGRICULTURE,
    "metal": CN_METALS,
    "energy": CN_ENERGY,
    "indices": CN_INDICES,
}

DEFAULT_CN_GROUP_RISK_FACTORS = {
    "agriculture": 0.08,
    "metal": 0.08,
    "energy": 0.08,
    "indices": 0.05,
}
