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
Script to generate aligned dataframe from many contract file with
adjusted prices.

This script could be used for the CSI data(https://www.csidata.com/)
or the data from cn exchange.
"""

import os

from greenturtle.constants.future import varieties
from greenturtle.data.preprocess import align
from greenturtle.util.logging import logging


logger = logging.get_logger()

SRC_DIR = "./continuous/us/csidata_adjusted_greenturtle"
DST_DIR = "./align/us"


if __name__ == "__main__":

    if not os.path.exists(DST_DIR):
        os.mkdir(DST_DIR)

    varieties_path = {}
    for group in varieties.US_VARIETIES.values():
        for variety in group:
            file_path = os.path.join(SRC_DIR, f"{variety}.csv")
            if os.path.exists(file_path):
                varieties_path[variety] = file_path

    a = align.Align(varieties_path, DST_DIR)
    a.align_all()
