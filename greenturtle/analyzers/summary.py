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

"""summary for analyzer."""

import abc


class BaseSummary:
    """base summary class."""
    def __init__(self):
        pass

    @abc.abstractmethod
    def to_string(self):
        """generate the string representation of the summary."""
        raise NotImplementedError

    def print(self):
        """print the message"""
        message = self.to_string()
        print(message)


class ReturnSummary(BaseSummary):
    """summary for return."""

    def __init__(self,
                 total_return=None,
                 annual_return=None,
                 years_return=None,
                 days_return=None):
        super().__init__()

        self.total_return = total_return
        self.annual_return = annual_return

        if years_return is not None:
            self.years_return = years_return
        else:
            self.years_return = None

        if days_return is not None:
            self.days_return = days_return
        else:
            self.days_return = None

    def to_string(self):
        """string of the return summary"""

        message = ""
        if self.total_return is not None:
            message += f"total Return: {self.total_return:.2f}%\n"

        if self.annual_return is not None:
            message += f"annual Return: {self.annual_return:.2f}%\n"

        if self.years_return is not None:
            for year in self.years_return:
                message += f"{year}: {self.years_return[year]:.2f}%\n"

        if message != "":
            # add the head of return summary
            message = "********** return summary **********\n" + message

        return message


class SharpeRatioSummary(BaseSummary):
    """summary for sharpe ratio."""

    def __init__(self, sharpe_ratio=None):
        super().__init__()

        self.sharpe_ratio = sharpe_ratio

    def to_string(self):
        """string of the sharpe ratio."""

        message = ""
        if self.sharpe_ratio is not None:
            message += f"Sharpe Ratio: {self.sharpe_ratio:.3f}\n"

        if message != "":
            # add the head of sharpe ratio summary
            message = "********** sharpe ratio summary **********\n" + message

        return message


class MaxDrawDownSummary(BaseSummary):
    """summary for max draw down."""

    def __init__(self, max_draw_down=None):
        super().__init__()

        self.max_draw_down = max_draw_down

    def to_string(self):
        """string of the max draw down."""

        message = ""
        if self.max_draw_down is not None:
            message += f"Max Draw Down: {self.max_draw_down:.1f}%\n"

        if message != "":
            # add the head of max draw down summary
            message = "********** max draw down summary **********\n" + message

        return message


class LeverageRatioSummary(BaseSummary):
    """summary for leverage ratio."""

    def __init__(self, leverage_ratio=None):
        super().__init__()

        self.leverage_ratio = leverage_ratio

    def to_string(self):
        """string of the leverage ratio."""

        message = ""
        if self.leverage_ratio is not None:
            message += f"leverage ratio: {self.leverage_ratio:.2f}\n"

        if message != "":
            # add the head of leverage ratio summary
            header = "********** leverage ratio summary **********\n"
            message = header + message

        return message


class TradeSummary(BaseSummary):
    """summary for the trades."""

    # pylint: disable=too-many-positional-arguments,too-many-arguments
    def __init__(self,
                 net=None,
                 gross=None,
                 won=None,
                 lost=None,
                 trader_number=None,
                 won_trader_number=None):
        super().__init__()

        self.net = net
        self.gross = gross
        self.won = won
        self.lost = lost
        self.trader_number = trader_number
        self.win_trader_number = won_trader_number

    def to_string(self):
        """string of the trade."""

        message = ""
        if self.net is not None:
            message += f"net: {self.net:.0f}\n"

        if self.gross is not None:
            message += f"gross: {self.gross:.0f}\n"

        if self.won is not None:
            message += f"won: {self.won:.0f}\n"

        if self.lost is not None:
            message += f"lost: {self.lost:.0f}\n"

        if (self.net is not None) and (self.gross is not None):
            commission = self.gross - self.net
            message += f"commission: {commission:.0f}\n"

        if self.trader_number is not None:
            message += f"trader_number: {self.trader_number:.0f}\n"

        if self.win_trader_number is not None:
            message += f"win_trader_number: {self.win_trader_number:.0f}\n"

        if (
                (self.trader_number is not None) and
                (self.win_trader_number is not None)
        ):
            win_ratio = 1.0 * self.win_trader_number / self.trader_number
            message += f"win_ratio: {win_ratio:.2f}\n"

        if message != "":
            # add the head of trade summary
            message = "********** trade summary **********\n" + message

        return message


class PositionsPNLSummary(BaseSummary):
    """summary for the profit and lost for positions."""

    def __init__(self, positions_pnl=None):
        super().__init__()

        self.positions_pnl = positions_pnl

    def to_string(self):
        """string of the profit and lost for positions."""
        message = ""

        if self.positions_pnl is not None:
            for name in self.positions_pnl:
                pln = self.positions_pnl[name]
                net = pln["net"]
                profit = pln["profit"]
                lost = pln["lost"]
                comm = pln["gross"] - pln["net"]
                trade_number = pln["trade_number"]
                message += f"{name}, " + \
                           f"net: {net:.0f}, " + \
                           f"profit: {profit:.0f}, " + \
                           f"lost: {lost:.0f}, " + \
                           f"comm: {comm:.0f}, " + \
                           f"trader number: {trade_number}\n"

        if message != "":
            # add the head of trade summary
            message = "********** trade summary **********\n" + message

        return message


class Summary(BaseSummary):
    """summary for backtesting."""
    def __init__(self):
        super().__init__()

        self.return_summary = None
        self.sharpe_ratio_summary = None
        self.max_draw_down_summary = None
        self.leverage_ratio_summary = None
        self.trade_summary = None
        self.positions_pnl_summary = None

    def to_string(self):
        """string of the summary."""
        message = ""

        if self.return_summary is not None:
            message += self.return_summary.to_string()

        if self.sharpe_ratio_summary is not None:
            message += self.sharpe_ratio_summary.to_string()

        if self.max_draw_down_summary is not None:
            message += self.max_draw_down_summary.to_string()

        if self.leverage_ratio_summary is not None:
            message += self.leverage_ratio_summary.to_string()

        if self.trade_summary is not None:
            message += self.trade_summary.to_string()

        if self.positions_pnl_summary is not None:
            message += self.positions_pnl_summary.to_string()

        if message != "":
            message = "\n" + message

        return message
