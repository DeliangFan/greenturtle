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

"""WeChat notifier."""

import wxpusher


# pylint: disable=too-few-public-methods
class WechatNotifier:
    """Wechat notifier."""

    def __init__(self, wechat_conf):
        if 'uid' not in wechat_conf:
            raise ValueError('WeChat uid not set')
        if 'token' not in wechat_conf:
            raise ValueError('WeChat token not set')

        self.token = wechat_conf.token
        self.uid = wechat_conf.uid

    def send_message(self, message):
        """send message"""
        wxpusher.WxPusher.send_message(content=message,
                                       uids=[self.uid],
                                       token=self.token)
