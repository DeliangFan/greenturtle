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


"""logging module for greenturtle."""

import datetime
import logging
import os
import sys


LOGGER_NAME = "greenturtle"
LOGGER_PATH = "/var/log/greenturtle"


def init_logger():
    """Init logger for greenturtle."""
    logger = logging.getLogger(LOGGER_NAME)

    # Set the threshold logging level of the logger to INFO.
    logger.setLevel(logging.INFO)

    # Set the log format.
    formatter = logging.Formatter(
        '%(asctime)s:%(levelname)s:%(name)s:%(module)s  %(message)s')

    # Create a file-based handler that writes the log entries into the
    # log file.
    if not os.path.exists(LOGGER_PATH):
        os.mkdir(LOGGER_PATH)

    suffix = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = get_log_file_name(suffix)
    file_handler = logging.FileHandler(file_name)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Create a stream-based handler that writes the log entries into the
    # standard output stream.
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)


def get_log_file_name(suffix):
    """get the log file name according to the path and current time."""
    name = f"{LOGGER_PATH}/{LOGGER_NAME}-{suffix}.log"
    return name


def get_logger():
    """get the greenturtle logger."""
    logger = logging.getLogger(LOGGER_NAME)
    return logger
