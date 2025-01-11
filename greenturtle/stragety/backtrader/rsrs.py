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

""" RSRS class strategy for backtrader"""

import numpy as np
from sklearn.linear_model import LinearRegression

from greenturtle.stragety.backtrader import base


class RSRSStrategy(base.BaseStrategy):

    """
    RSRS class strategy for backtrader.

    RSRS is short for resistence support relative strength.

    光大证券 <基于阻力支撑相对强度的市场择时>
    """

    def __init__(self, period=18, upper=1.1, lower=0.7):
        super().__init__()
        self.period = period
        # according to the experiment in btc, the performance depends a lot
        # on the upper and lower parameters.
        self.upper = upper
        self.lower = lower

    def compute_rsrs(self):
        """compute teh rsrs value."""
        high = self.data.high.get(size=self.period)
        low = self.data.low.get(size=self.period)

        if len(high) == 0 or len(low) == 0:
            return None

        x = np.array(low).reshape(-1, 1)
        y = np.array(high).reshape(-1, 1)
        lr = LinearRegression().fit(x, y)
        lr.predict(x)
        rsrs = lr.coef_[0]
        return rsrs

    def next(self):
        if self.order:
            return

        rsrs = self.compute_rsrs()
        if rsrs is None:
            return

        if self.position:
            if rsrs <= self.lower:
                self.order_target_percent(target=0)
        # not in the market
        else:
            if rsrs >= self.upper:
                self.order_target_percent(target=1.0)
