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
Script to generate continuous dataframe from many contract file with
adjusted prices.

This script could be used for the CSI data(https://www.csidata.com/)
or the data from cn exchange.
"""

import datetime
import os

from greenturtle.constants.future import varieties
from greenturtle.data.preprocess import generate_continuous
from greenturtle.util.logging import logging


logger = logging.get_logger()

SRC_DIR = "./contract/cn"
DST_DIR = "./continuous/cn/exchange_adjusted_greenturtle"


if __name__ == "__main__":

    for group in varieties.CN_VARIETIES.values():
        for variety in group:
            src_dir = os.path.join(SRC_DIR, variety)
            if not os.path.exists(src_dir):
                continue

            # initiate the process
            p = generate_continuous.GenerateContinuousFromAKShare(
                variety,
                fromdate=datetime.datetime(2005, 2, 1),
                todate=datetime.datetime(2025, 2, 6),
                src_dir=src_dir,
                dst_dir=DST_DIR)

            p.generate()
