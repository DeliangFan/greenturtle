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

"""
scripts used to cancel or modify the order in case of bugs.

    value & cash
    - get cash: broker.get_cash()
    - get value: broker.get_value()

    order:
    - get order: broker.get_orders_open()
    - get open order: broker.get_orders()
    - cancel order: broker.cancel_order()

    positions:
    - get positions: broker.get_positions()

    buy & sell:
    - buy:  broker.buy(None, None, 1, **kwargs)
    - sell: broker.sell(None, None, 1, **kwargs)
    # kwargs = {"variety": "C", "desired_size": 1}
"""

from greenturtle.brokers import tqbroker
from greenturtle.util import config
from greenturtle.util.notifier import fake


def get_tq_broker():
    """get tq broker"""
    conf = config.load_config("/etc/greenturtle/greenturtle.yaml")
    notifier = fake.FakeNotifier()
    broker = tqbroker.TQBroker(conf=conf, notifier=notifier)
    return broker


if __name__ == "__main__":
    b = get_tq_broker()
    print(b.account_overview())
    b.close()
