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

"""back broker."""

from backtrader import brokers


class BackBroker(brokers.BackBroker):
    """back broker."""
    def __init__(self):
        super().__init__()
        # Set our desired cash start
        self.setcash(1000000)
        # Set short cash
        self.set_shortcash(False)
        # Disable cheat on close
        self.set_coc(False)

    def account_overview(self):
        """Return account overview."""
        value = self.get_value()
        cash = self.get_cash()
        txt = f"Back broker: value: {value}, cash: {cash}"

        for symbol, position in self.positions.items():
            txt += f", {symbol}: {position.size}"

        return txt
