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


class ContractNotFound(GreenTurtleBaseException):
    """contract not found error."""
    msg_fmt = "contract not found error."


class GroupNameNotFound(GreenTurtleBaseException):
    """group name not found error."""
    msg_fmt = "group name not found error."


class AutoMarginNotFound(GreenTurtleBaseException):
    """auto margin not found error."""
    msg_fmt = "auto margin not found error."


class MultiplierNotFound(GreenTurtleBaseException):
    """multiplier not found error."""
    msg_fmt = "multiplier not found error."


class AccountBankruptcy(GreenTurtleBaseException):
    """account bankruptcy error."""
    msg_fmt = "account bankruptcy error."


class DataPriceHighAbnormalError(GreenTurtleBaseException):
    """Data high abnormal error."""
    msg_fmt = "Data high price abnormal error."


class DataPriceLowAbnormalError(GreenTurtleBaseException):
    """Data low abnormal error."""
    msg_fmt = "Data low price abnormal error."


class DataPriceNonPositiveError(GreenTurtleBaseException):
    """Data price non positive error."""
    msg_fmt = "Data price non positive error."


class DataPriceExceedDailyLimitError(GreenTurtleBaseException):
    """Data price exceed daily limit error."""
    msg_fmt = "Data price exceed daily limit error."


class DataPriceInvalidTypeError(GreenTurtleBaseException):
    """Data price invalid type error."""
    msg_fmt = "Data price invalid type error."


class DataContractAbnormalError(GreenTurtleBaseException):
    """Data contract abnormal error."""
    msg_fmt = "Data contract abnormal error."


class DownloadDataError(GreenTurtleBaseException):
    """Download data error."""
    msg_fmt = "Download data error."


class SourceCountryNotSupportedError(GreenTurtleBaseException):
    """source and country not supported error."""
    msg_fmt = "Source and country not supported error."


class ExchangeNotSupportedError(GreenTurtleBaseException):
    """exchange not supported error."""
    msg_fmt = "Exchange not supported error."


class DataInvalidExpireError(GreenTurtleBaseException):
    """Data invalid expire error."""
    msg_fmt = "Data invalid expire error."


class ContinuousContractOrderAbnormalError(GreenTurtleBaseException):
    """Continuous contract order error."""
    msg_fmt = "Continuous contract order error."


class ContinuousContractNotFound(GreenTurtleBaseException):
    """Continuous contract not found error."""
    msg_fmt = "Continuous contract not found error."


class ValidateTradingDayError(GreenTurtleBaseException):
    """Validate trading day error"""
    msg_fmt = "Validate trading day error."


class ValidateRiskFactorError(GreenTurtleBaseException):
    """Validate risk factor error"""
    msg_fmt = "Validate risk factor error."


class ValidateGroupRiskFactorError(GreenTurtleBaseException):
    """Validate group risk factor error"""
    msg_fmt = "Validate group risk factor error."
