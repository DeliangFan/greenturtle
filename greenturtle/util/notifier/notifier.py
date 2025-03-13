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

"""get notifier"""

from greenturtle.util.notifier import fake
from greenturtle.util.notifier import telegram
from greenturtle.util.notifier import wechat


def get_notifier(conf):
    """get notifier according to conf"""

    if 'notifier' not in conf:
        raise ValueError("notifier not found")

    notifier_conf = conf.notifier
    if 'telegram' in notifier_conf:
        notifier = telegram.TelegramNotifier(notifier_conf.telegram)
    elif 'wechat' in notifier_conf:
        notifier = wechat.WechatNotifier(notifier_conf.wechat)
    else:
        notifier = fake.FakeNotifier()

    return notifier
