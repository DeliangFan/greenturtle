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

"""telegram notifier."""

import telebot


# pylint: disable=too-few-public-methods
class TelegramNotifier:
    """Telegram notifier."""

    def __init__(self, tg_conf):
        if not hasattr(tg_conf, 'bot_token'):
            raise ValueError('Telegram bot token not set')

        if not hasattr(tg_conf, 'chat_id'):
            raise ValueError('Telegram chat id not set')

        bot_token = tg_conf.bot_token
        self.chat_id = tg_conf.chat_id
        self.bot = telebot.TeleBot(bot_token)

    def send_message(self, message):
        """send message"""
        self.bot.send_message(chat_id=self.chat_id, text=message)
