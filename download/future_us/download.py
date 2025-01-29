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

import greenturtle.constants.future as future_const
import greenturtle.data.backtrader.future as future_data


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")


if __name__ == '__main__':
    # create output directory
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    for category_name, category_value in future_const.FUTURE.items():

        category_dir = os.path.join(OUTPUT_DIR, category_name)
        if not os.path.exists(category_dir):
            os.makedirs(category_dir)

        for name, future in category_value.items():
            # pylint: disable=invalid-name
            yahoo_code = future[future_const.YAHOO_CODE]

            margin_requirement_ratio = \
                future[future_const.MARGIN_REQUIREMENT_RATIO]

            df = future_data.get_data_frame_from_yahoo_finance(
                yahoo_code=yahoo_code,
                name=name,
                category=category_name,
                contract_unit=future[future_const.CONTRACT_UNIT],
                margin_requirement_ratio=margin_requirement_ratio,
            )

            df.to_csv(os.path.join(category_dir, f"{name}.csv"))
