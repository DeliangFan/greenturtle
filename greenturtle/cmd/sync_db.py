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

""" Manage scripts, for example run storage database migration."""

import argparse

from greenturtle.db import api
from greenturtle.util import config


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


def main():
    """main function"""

    # load config
    args = parser.parse_args()
    conf = config.load_config(args.conf)

    # do create database tables
    manager = api.DBManager(conf.db)
    manager.create_all()


if __name__ == "__main__":
    main()
