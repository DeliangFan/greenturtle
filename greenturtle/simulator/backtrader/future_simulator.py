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

"""simulator for future because of contract and margin."""

from backtrader import comminfo

import greenturtle.constants.future as future_const
from greenturtle import exception
from greenturtle.simulator.backtrader import simulator


class FutureSimulator(simulator.Simulator):
    """future simulator"""
    def __init__(self, cash=1000000, slippage=0, plot=False):
        super().__init__(cash=cash, slippage=slippage, plot=plot)

    def set_commission(self, commission=4, margin=None, mult=1.0, name=None):
        """set commission for future by name."""
        self.cerebro.broker.setcommission(
            commission=commission,
            margin=margin,
            mult=mult,
            commtype=comminfo.CommInfoBase.COMM_FIXED,
            stocklike=False,
            name=name,
        )

    @staticmethod
    def get_auto_margin(name):
        """get auto margin for future by name."""
        for category in future_const.FUTURE.values():
            for future_name, future in category.items():
                if future_name == name:
                    return future[future_const.AUTO_MARGIN]

        # raise exception if not found
        raise exception.AutoMarginNotFound

    @staticmethod
    def get_multiplier(name):
        """get multiplier for future by name."""
        for category in future_const.FUTURE.values():
            for future_name, future in category.items():
                if future_name == name:
                    return future[future_const.MULTIPLIER]

        # raise exception if not found
        raise exception.MultiplierNotFound

    def set_default_commission_by_name(self, name, commission=4):
        """set default commission by name."""
        multiplier = self.get_multiplier(name)
        auto_margin = self.get_auto_margin(name)

        self.cerebro.broker.setcommission(
            commission=commission,
            mult=multiplier,
            commtype=comminfo.CommInfoBase.COMM_FIXED,
            stocklike=False,
            automargin=auto_margin,
            name=name,
        )
