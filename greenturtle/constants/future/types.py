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

"""some constants like types and meta for future"""


# price constants columns constants
ID = "id"
DATETIME = "datetime"
OPEN = "open"
HIGH = "high"
LOW = "low"
CLOSE = "close"
ORI_OPEN = "ori_open"
ORI_HIGH = "ori_high"
ORI_LOW = "ori_low"
ORI_CLOSE = "ori_close"
TURN_OVER = "turn_over"

# other columns constants
CONTRACT = "contract"
EXPIRE = "expire"
VOLUME = "volume"
TOTAL_VOLUME = "total_volume"
OPEN_INTEREST = "open_interest"
TOTAL_OPEN_INTEREST = "total_open_interest"
SETTLE = "settle"
PRE_SETTLE = "pre_settle"
VARIETY = "variety"
# adjust factor
ADJUST_FACTOR = "adjust_factor"
# valid, used for align and padding
VALID = "valid"

# yahoo dedicated code constant
YAHOO_CODE = "yahoo_code"

# others future constants
UNKNOWN = "unknown"
MULTIPLIER = "multiplier"
AUTO_MARGIN = "auto_margin"
DESCRIPTION = "description"

# portfolio constants
PORTFOLIO_TYPE_ATR = "atr"
PORTFOLIO_TYPE_AVERAGE = "average"

# datetime format for future
DATE_FORMAT = "%Y%m%d"

# Country
CN = "CN"
US = "US"

# Data Source
CSI = "CSI"
AKSHARE = "akshare"

# csv structure for contract
CONTRACT_COLUMN = [
    CONTRACT,
    EXPIRE,
    OPEN,
    HIGH,
    LOW,
    CLOSE,
    VOLUME,
    OPEN_INTEREST,
    TOTAL_VOLUME,
    TOTAL_OPEN_INTEREST,
]

CONTRACT_DATA_DTYPE = {
    DATETIME: str,
    CONTRACT: str,
    EXPIRE: str,
    OPEN: float,
    HIGH: float,
    LOW: float,
    CLOSE: float,
    VOLUME: int,
    OPEN_INTEREST: int,
    TOTAL_VOLUME: int,
    TOTAL_OPEN_INTEREST: int,
}

# csv structure for continuous
CONTINUOUS_COLUMN = [
    CONTRACT,
    EXPIRE,
    OPEN,
    HIGH,
    LOW,
    CLOSE,
    ORI_OPEN,
    ORI_HIGH,
    ORI_LOW,
    ORI_CLOSE,
    VOLUME,
    TOTAL_VOLUME,
    OPEN_INTEREST,
    TOTAL_OPEN_INTEREST,
    VALID,
]

CONTINUOUS_LINES = (
    ORI_OPEN,
    ORI_HIGH,
    ORI_LOW,
    ORI_CLOSE,
    TOTAL_VOLUME,
    TOTAL_OPEN_INTEREST,
    VALID,
)

CONTINUOUS_DATA_DTYPE = {
    DATETIME: str,
    CONTRACT: str,
    EXPIRE: str,
    OPEN: float,
    HIGH: float,
    LOW: float,
    CLOSE: float,
    ORI_OPEN: float,
    ORI_HIGH: float,
    ORI_LOW: float,
    ORI_CLOSE: float,
    VOLUME: int,
    OPEN_INTEREST: int,
    TOTAL_VOLUME: int,
    TOTAL_OPEN_INTEREST: int,
    VALID: int,
}

# month codes alphabets to number constants
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

# month codes number to alphabets constants
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
