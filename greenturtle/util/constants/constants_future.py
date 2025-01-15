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

FUTURE = {
    "agriculture": AGRICULTURE,
}
