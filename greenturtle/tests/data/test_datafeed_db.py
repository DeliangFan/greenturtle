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

"""unittest for datafeed/db.py"""

import datetime
import unittest

from greenturtle.db import models
from greenturtle.data.datafeed import db
from greenturtle import exception


class TestContinuousContractDB(unittest.TestCase):
    """unittest for ContinuousContractDB class"""

    def test_get_sort_dates(self):
        """test for _get_sort_dates"""
        c1 = models.ContinuousContract(date=datetime.datetime(2025, 3, 24))
        c2 = models.ContinuousContract(date=datetime.datetime(2025, 3, 26))
        c3 = models.ContinuousContract(date=datetime.datetime(2025, 3, 25))
        continuous_contracts = [c1, c2, c3]
        # pylint:disable=protected-access
        actual = db.ContinuousContractDB._get_sort_dates(continuous_contracts)
        self.assertEqual([c2.date, c3.date, c1.date], actual)

    def test_get_continuous_contracts_dict(self):
        """test for _get_continuous_contracts_dict"""
        c = models.ContinuousContract(date=datetime.datetime(2025, 3, 24))
        # pylint:disable=protected-access
        actual = db.ContinuousContractDB._get_continuous_contracts_dict([c])
        self.assertEqual({c.date: c}, actual)

    def test_validate_trading_dates(self):
        """test _validate_trading_dates"""
        trading_dates = [datetime.datetime(2025, 3, 24)]

        # test with validate success
        dates = [datetime.datetime(2025, 3, 24)]
        # pylint:disable=protected-access
        db.ContinuousContractDB._validate_trading_dates(dates, trading_dates)

        # test with validate failed
        dates = [datetime.datetime(2025, 3, 27)]
        # pylint:disable=protected-access
        self.assertRaises(exception.ValidateTradingDayError,
                          db.ContinuousContractDB._validate_trading_dates,
                          dates, trading_dates)

    def test_validate(self):
        """test validate"""
        datafeed = db.ContinuousContractDB()

        # test validate success
        c1 = models.ContinuousContract(
            date=datetime.datetime(2025, 3, 24),
            open=10,
            high=11,
            low=9,
            close=10,
        )
        c2 = models.ContinuousContract(
            date=datetime.datetime(2025, 3, 25),
            open=11,
            high=12,
            low=10,
            close=11,
        )
        datafeed.validate([c1, c2])

        # test validate failed
        c2 = models.ContinuousContract(
            date=datetime.datetime(2025, 3, 25),
            open=20,
            high=22,
            low=20,
            close=21,
        )
        self.assertRaises(exception.DataPriceExceedDailyLimitError,
                          datafeed.validate,
                          [c1, c2])

        # adjust_price
        # align_and_padding
