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

"""greenturtle exception handling"""

from greenturtle.util.logging import logging


logger = logging.get_logger()


class GreenTurtleBaseException(Exception):

    """Green turtle base exception."""

    msg_fmt = "greenturtle base exception."

    def __init__(self, message=None):
        try:
            if not message:
                message = self.msg_fmt
            else:
                message = str(message)

            # pylint: disable=broad-except
        except Exception:
            self._log_exception(message)

        super().__init__(message)

    def _log_exception(self, message):
        logger.exception(msg=message)


class SymbolUnexpectedIntersectionError(GreenTurtleBaseException):
    """symbol unexpected intersection error."""
    msg_fmt = "symbol unexpected intersection error."
