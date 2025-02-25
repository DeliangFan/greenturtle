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

""" RSRS indicator for backtrader"""


from backtrader.indicator import Indicator
import numpy as np
from sklearn.linear_model import LinearRegression


class RSRS(Indicator):

    """RSRS indicator."""

    lines = ('rsrs',)
    params = (('period', 18),)

    def __init__(self):
        super().__init__()
        self.period = self.p.period

    def next(self):
        """compute teh rsrs value."""

        x = self.data.low.get(size=self.period)
        y = self.data.high.get(size=self.period)
        if len(x) == 0 or len(y) == 0:
            # pylint: disable=no-member
            self.lines.rsrs[0] = -1
            return

        x = np.array(x)
        y = np.array(y)
        lr = LinearRegression()
        lr.fit(x.reshape(-1, 1), y)

        # pylint: disable=no-member
        self.lines.rsrs[0] = lr.coef_[0]
