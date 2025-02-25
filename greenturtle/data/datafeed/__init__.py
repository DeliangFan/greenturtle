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
Data feed for future.

Greenturtle defines the data structure both in the csv file and datafeed,
which means that these download scripts should convert the data into the
desired format so that the cerebro could consume the data with datafeed.

Data structure.
- index, datetime with "%Y%m%d"
- column contract: contract name,
- column expire: expire date
- column open: open price, the open price should be adjusted price
- column high: high price, the high price should be adjusted price
- column low: low price, the low price should be adjusted price
- column close: close price, the close price should be adjusted price
- column ori_open: original open price
- column ori_high: original high price
- column ori_low: original low price
- column ori_close: original close price
- column volume: the amount of volume
- column total_volume: total volume of all contracts
- column open_interest: open interest
- column total_open_interest: total open interest of all contracts
- column valid: row data valid or not
"""
