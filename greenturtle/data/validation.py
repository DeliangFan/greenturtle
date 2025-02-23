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

"""validation for data"""

from greenturtle import exception


def validate_price(open_price, high_price, low_price, close_price):
    """validate price"""

    validate_price_type(open_price, high_price, low_price, close_price)
    validate_positive_price(open_price)
    validate_positive_price(high_price)
    validate_positive_price(low_price)
    validate_positive_price(close_price)
    validate_high_price(open_price, high_price, low_price, close_price)
    validate_low_price(open_price, high_price, low_price, close_price)


def validate_price_type(open_price, high_price, low_price, close_price):
    """validate price type, price could only be int or float type"""
    if not (
            isinstance(open_price, (int, float)) and
            isinstance(high_price, (int, float)) and
            isinstance(low_price, (int, float)) and
            isinstance(close_price, (int, float))
    ):
        raise exception.DataPriceInvalidTypeError


def validate_high_price(open_price, high_price, low_price, close_price):
    """validate data high price"""
    if (
            (high_price < open_price) or
            (high_price < low_price) or
            (high_price < close_price)
    ):
        raise exception.DataPriceHighAbnormalError


def validate_low_price(open_price, high_price, low_price, close_price):
    """validate data low price"""
    if (
            (low_price > open_price) or
            (low_price > high_price) or
            (low_price > close_price)
    ):
        raise exception.DataPriceLowAbnormalError


def validate_positive_price(price):
    """validate data price non-negative"""

    if price <= 0:
        raise exception.DataPriceNonPositiveError
