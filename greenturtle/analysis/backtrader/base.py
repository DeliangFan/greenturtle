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

"""Experiment to benchmark the MACD performance on cryptocurrencies."""

import math

import backtrader as bt
from matplotlib import pyplot
import pandas as pd

from greenturtle.util import panda_util


def do_analysis(datas, strategy):
    """analysis the performance according to the data and strategy."""

    # initiate the panda options.
    panda_util.init_pandas()

    # setting the strategy and data.
    analysis = Analysis()
    analysis.add_strategy(strategy)
    for name, data in datas:
        analysis.add_data(data, name=name)

    # show the result.
    result = analysis.run()
    analysis.show(result)


class Analysis():

    """Basic analysis class for backtrader."""

    def __init__(self):
        self.cerebro = bt.Cerebro()

        # add analyzer
        self.cerebro.addanalyzer(
            bt.analyzers.AnnualReturn,
            _name="AnnualReturn")
        self.cerebro.addanalyzer(
            bt.analyzers.TimeReturn,
            _name="TimeReturn")
        self.cerebro.addanalyzer(
            bt.analyzers.Returns,
            _name="Returns",
            tann=252)
        self.cerebro.addanalyzer(
            bt.analyzers.DrawDown,
            _name="DrawDown")
        self.cerebro.addanalyzer(
            bt.analyzers.SharpeRatio_A,
            _name="SharpeRatio_A")
        self.cerebro.addanalyzer(
            bt.analyzers.TradeAnalyzer,
            _name="TradeAnalyzer")

        # Set the commission
        self.cerebro.broker.setcommission(commission=0.001)
        self.cerebro.broker.set_slippage_perc(perc=0.001)

        # Set our desired cash start
        self.cerebro.broker.setcash(1000000.0)

        # what's cheat on close
        self.cerebro.broker.set_coc(True)

        # Add a FixedSize sizer according to the stake
        self.cerebro.addsizer(bt.sizers.FixedSize, stake=1)

    def add_strategy(self, strategy):
        """add strategy to cerebro."""
        self.cerebro.addstrategy(strategy)

    def add_data(self, data, name=None):
        """add data to cerebro."""
        self.cerebro.adddata(data, name=name)

    def run(self):
        """run the analysis."""
        # Print out the starting conditions
        value = self.cerebro.broker.getvalue()
        print(f"Starting Portfolio Value: {value:.2f}")

        # Run over everything
        result = self.cerebro.run()

        # Print out the final result
        value = self.cerebro.broker.getvalue()
        print(f"Final Portfolio Value: {value:.2f}")

        return result

    def show_return(self, result):
        """analyze the return."""
        returns = result[0].analyzers.Returns.get_analysis()
        total_return = math.exp(returns["rtot"]) * 100
        annual_return = returns["rnorm"] * 100
        print(f"total return: {total_return:0.1f}%")
        print(f"annual return: {annual_return:0.1f}%")

    def show_max_draw_down(self, result):
        """analyze the max draw down."""
        draw_down = result[0].analyzers.DrawDown.get_analysis()
        max_draw_down = draw_down["max"]["drawdown"]
        print(f"Max draw down: {max_draw_down:0.1f}%")

    def show_sharpe_ratio(self, result):
        """analyze the sharpe ratio."""
        sharpe = result[0].analyzers.SharpeRatio_A.get_analysis()
        sharpe_ratio = sharpe["sharperatio"]
        print(f"Sharpe Ratio: {sharpe_ratio:0.3f}")

    def show_trade_analyzer(self, result):
        """analyze the trade."""

        trade_analyzer = result[0].analyzers.TradeAnalyzer.get_analysis()

        if (
                ("pnl" not in trade_analyzer) or
                ("total" not in trade_analyzer) or
                ("won" not in trade_analyzer) or
                ("lost" not in trade_analyzer)
        ):
            return

        total = trade_analyzer["total"]["total"]
        net = trade_analyzer["pnl"]["net"]["total"]
        gross = trade_analyzer["pnl"]["gross"]["total"]
        comm = gross - net

        won_total = trade_analyzer["won"]["total"]
        won_ratio = won_total * 1.0 / total
        won_profit_total = trade_analyzer["won"]["pnl"]["total"]
        won_profit_average = trade_analyzer["won"]["pnl"]["average"]

        lost_total = trade_analyzer["lost"]["total"]
        lost_profit_total = trade_analyzer["lost"]["pnl"]["total"]
        lost_profit_average = trade_analyzer["lost"]["pnl"]["average"]

        print(
            f"net: {net:.0f}, won: {won_profit_total:.0f}, " +
            f"lost: {lost_profit_total:.0f}, comm: {comm:.0f}")
        print(
            f"total trade number: {total}, won: {won_total}," +
            f"lost: {lost_total}, ratio: {won_ratio:.2f}")
        print(
            f"won profit average: {won_profit_average:.0f}, " +
            f"lost profit average: {lost_profit_average:.0f}")

    def plot_figure(self, result):
        """plot the figure."""

        ret = pd.Series(result[0].analyzers.TimeReturn.get_analysis())  #

        # create the canvas
        _, ax1 = pyplot.subplots(figsize=(20, 12), dpi=200)
        ax1.set_title("crypto profit", fontsize=30)
        pyplot.grid(True, linestyle="--")

        ax1.plot(
            (ret + 1).cumprod().index,
            (ret + 1).cumprod().values,
            "r-",
            label="profit")

        pyplot.show()

    def show(self, result):
        """show the backtest result."""
        print("*************** Overview *************")

        # show the return.
        self.show_return(result)
        # show the max draw down.
        self.show_max_draw_down(result)
        # show the sharpe ratio
        self.show_sharpe_ratio(result)
        # show the trade analyzer
        self.show_trade_analyzer(result)
        # plot the figures.
        self.plot_figure(result)
