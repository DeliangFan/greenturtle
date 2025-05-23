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
from greenturtle.stragety import base


class MIMStrategy(base.BaseStrategy):

    """ MIM class strategy for backtrader"""

    def __init__(self, *args, period=100, **kwargs):
        super().__init__(*args, **kwargs)
        self.movs = {}
        for name in self.names:
            data = self.getdatabyname(name)
            self.movs[name] = MovAv.Exponential(data, period=period)

    def is_buy_to_open(self, name):
        """determine whether a position should buy to open or not."""
        mov = self.movs[name]
        data = self.symbols_data[name]
        return data[0] > mov[0]

    def is_sell_to_close(self, name):
        """determine whether a position should sell to close or not."""
        mov = self.movs[name]
        data = self.symbols_data[name]
        return data[0] < mov[0]

    def is_sell_to_open(self, name):
        """determine whether a position should sell to open or not."""
        return False

    def is_buy_to_close(self, name):
        """determine whether a position should buy to close or not."""
        return False
