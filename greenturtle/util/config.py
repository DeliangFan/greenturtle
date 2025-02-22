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

"""config utils"""

import munch
import yaml


def load_config(config_path):
    """load the config by path."""
    with open(config_path, encoding="utf-8") as f:
        # load the config and convert to object like config
        conf_dict = yaml.safe_load(f)
        conf = munch.DefaultMunch.fromDict(conf_dict)
        return conf
