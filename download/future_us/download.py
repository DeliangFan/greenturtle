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

"""script to download the us future data from yahoo finance"""

import os

from greenturtle.util.constants import constants_future
from greenturtle.util import yf_util


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")


if __name__ == '__main__':
    # create output directory
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    for category_name, category_value in constants_future.FUTURE.items():

        category_dir = os.path.join(OUTPUT_DIR, category_name)
        if not os.path.exists(category_dir):
            os.makedirs(category_dir)

        for name, future in category_value.items():

            # pylint: disable=invalid-name
            yahoo_code = future[constants_future.YAHOO_CODE]

            df = yf_util.download_with_max_period(yahoo_code)
            df = yf_util.transform(df, yahoo_code)

            # add the future name and category
            df["name"] = name
            df["category"] = category_name
            df.to_csv(os.path.join(category_dir, f"{name}.csv"))
