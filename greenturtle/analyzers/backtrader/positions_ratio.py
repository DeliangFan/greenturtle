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

"""Positions ratio analyzer."""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)


import backtrader as bt


class PositionsRatio(bt.Analyzer):
    """This analyzer reports the positions ratio of the current set of
    datas.

    Methods:

      - get_analysis

        Returns a dictionary with returns as values and the datetime points for
        each return as keys
    """

    def next(self):
        """next function."""

        # pylint: disable=no-member
        strategy = self.strategy

        total_value = strategy.broker.get_value()

        # compute position value
        positions_value = 0
        for d in self.datas:
            positions_value = positions_value + strategy.broker.get_value([d])

        positions_ratio = positions_value / total_value
        self.rets[strategy.datetime.datetime()] = positions_ratio
