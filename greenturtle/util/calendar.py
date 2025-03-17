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
calendar module

The only reason that I create this module is that I could not find a
accurate open source project for china future trading. So I have to
reinvent the calendar wheel and maintain it in the project.
"""

import datetime

import chinese_calendar

from greenturtle import exception


START_DATE = datetime.date(year=2004, month=1, day=1)
END_DATE = datetime.date(year=2025, month=12, day=31)
RETRY = 30

# special days
SPECIAL_DATES = [
    datetime.date(year=2004, month=1, day=19),
    datetime.date(year=2004, month=1, day=20),
    datetime.date(year=2004, month=1, day=21),
    datetime.date(year=2005, month=2, day=7),
    datetime.date(year=2005, month=2, day=8),
    datetime.date(year=2006, month=1, day=26),
    datetime.date(year=2006, month=1, day=27),
    datetime.date(year=2024, month=2, day=9)
]


def validate_cn_date(date):
    """
    validate china date, only support the date between START_DATE and
    END_DATE
    """
    if date < START_DATE or date > END_DATE:
        raise exception.ValidateTradingDayError


def is_cn_trading_day(date):
    """
    check if it is a china trading day, a day is a trading day only if
    - it is a working day
    - it is weekday
    - exclude some special days
    """
    validate_cn_date(date)

    if chinese_calendar.is_holiday(date):
        return False

    if date.isoweekday() >= 6:
        return False

    if date in SPECIAL_DATES:
        return False

    return True


def get_cn_trading_days(start_date, end_date):
    """get the china trading days between start_date and end_date."""

    if start_date > end_date:
        raise exception.ValidateTradingDayError

    validate_cn_date(start_date)
    validate_cn_date(end_date)

    trading_days = []
    date = start_date

    while date <= end_date:
        if is_cn_trading_day(date):
            trading_days.append(date)
        date += datetime.timedelta(days=1)

    return trading_days


def get_cn_last_trading_day(date):
    """get cn last trading day before date"""
    # we must find the trading date within 30 days
    retry = RETRY
    date += datetime.timedelta(days=-1)

    while retry > 0:
        validate_cn_date(date)

        if is_cn_trading_day(date):
            return date

        date += datetime.timedelta(days=-1)
        retry = retry - 1

    raise exception.TradingDayNotFoundError


def get_cn_next_trading_day(date):
    """get cn next trading day after the date"""
    # we must find the trading date within 30 days
    retry = RETRY
    date += datetime.timedelta(days=1)

    while retry > 0:
        validate_cn_date(date)

        if is_cn_trading_day(date):
            return date

        date += datetime.timedelta(days=1)
        retry = retry - 1

    raise exception.TradingDayNotFoundError


def decision_regard_date():
    """return the date when making decision regard to"""
    today = datetime.date.today()

    # get the last trading day before today
    decision_date = get_cn_last_trading_day(today)

    # determine the decision date, and it's decided by the data
    if is_cn_trading_day(today):
        now = datetime.datetime.now().time()
        # check if it's closed time
        if now > datetime.time(15, 30):
            decision_date = today

    return decision_date
