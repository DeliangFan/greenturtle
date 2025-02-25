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

""" Buy and hold strategy for backtrader"""

from greenturtle.stragety import base


class BuyHoldStrategy(base.BaseStrategy):

    """ Buy and hold class strategy for backtrader

    Always buy the asset and never sell.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def is_buy_to_open(self, name):
        """determine whether a position should buy to open or not."""
        return True

    def is_sell_to_close(self, name):
        """determine whether a position should sell to close or not."""
        return False

    def is_sell_to_open(self, name):
        """determine whether a position should sell to open or not."""
        return False

    def is_buy_to_close(self, name):
        """determine whether a position should buy to close or not."""
        return False
