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

import munch
import yaml

from greenturtle.db import api


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
    args = parser.parse_args()

    with open(args.conf, encoding="utf-8") as f:
        # load the config and convert to object like config
        conf_dict = yaml.safe_load(f)
        conf = munch.DefaultMunch.fromDict(conf_dict)

        # do migrate
        manager = api.DBManager(conf)
        manager.create_all()
