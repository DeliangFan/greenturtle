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

""" MIM class strategy for backtrader"""

from backtrader.indicators import MovAv
from greenturtle.stragety.backtrader import base


class MIMStrategy(base.BaseStrategy):

    """ MIM class strategy for backtrader"""

    def __init__(self, period=100):
        super().__init__()
        self.movs = {}
        for name in self.names:
            data = self.getdatabyname(name)
            self.movs[name] = MovAv.Exponential(data, period=period)

    def should_buy(self, name):
        """determine whether a position should be bought or not."""
        mov = self.movs[name]
        data = self.symbols_data[name]
        return data[0] > mov[0]

    def should_sell(self, name):
        """determine whether a position should be sold or not."""
        mov = self.movs[name]
        data = self.symbols_data[name]
        return data[0] < mov[0]
