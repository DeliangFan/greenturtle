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

"""simulator for stock"""

from backtrader import comminfo

from greenturtle.simulator.backtrader import simulator


class StockSimulator(simulator.Simulator):
    """simulator for stock without margin."""

    def __init__(self, cash=1000000, slippage=0, plot=False):
        super().__init__(cash=cash, slippage=slippage, plot=plot)

    def set_commission(self,
                       commission=0.001,
                       margin=None,
                       mult=1.0,
                       name=None):
        """set commission."""
        self.cerebro.broker.setcommission(
            commission=commission,
            commtype=comminfo.CommInfoBase.COMM_PERC,
            stocklike=True)
