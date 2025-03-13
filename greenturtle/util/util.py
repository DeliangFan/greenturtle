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

"""some utility functions"""

from greenturtle.util.logging import logging


logger = logging.get_logger()


def get_group(variety, varieties):
    """get group name by variety name"""
    for group_name, group in varieties.items():
        for variety_name in group:
            if variety_name == variety:
                return group_name
    return None


def logger_and_notifier(notifier, msg):
    """logger and notifier"""
    logger.debug(msg)
    notifier.send_message(msg)
