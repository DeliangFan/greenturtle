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

"""greenturtle online service entrance"""

import argparse

# stupid tqsdk must be import first, otherwise it will flush the logs
# pylint: disable=unused-import
import tqsdk  # noqa F401

from greenturtle.util import config
from greenturtle.server import server


# pylint: disable=R0801
parser = argparse.ArgumentParser(
    prog='GreenTurtle for trading',
    description='scripts for create the database for greenturtle')

parser.add_argument(
    "--conf",
    type=str,
    default="/etc/greenturtle/greenturtle.yaml",
    help="config file for greenturtle"
)


if __name__ == "__main__":
    # load config
    args = parser.parse_args()
    conf = config.load_config(args.conf)

    # serving
    s = server.Server(conf)
    s.run()
