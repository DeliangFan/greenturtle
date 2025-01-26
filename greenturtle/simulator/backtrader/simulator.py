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
from greenturtle.util.logging import logging


logger = logging.get_logger()


def do_simulate(datas,
                strategy,
                *strategy_args,
                plot=True,
                commission=0.001,
                slippage=0.001,
                **strategy_kwargs):
    """analysis the performance according to the data and strategy."""

    # initiate the panda options.
    panda_util.init_pandas()

    # setting the strategy and data.
    analysis = Simulator(commission=commission, slippage=slippage)
    analysis.add_strategy(strategy, *strategy_args, **strategy_kwargs)
    for name, data in datas:
        analysis.add_data(data, name=name)

    # show the result.
    result = analysis.run()
    analysis.show(result, plot=plot)

    return analysis


class Simulator:

    """Basic analysis class for backtrader."""

    def __init__(self, commission=0.001, slippage=0.001):
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
        self.cerebro.broker.setcommission(commission=commission)
        self.cerebro.broker.set_slippage_perc(perc=slippage)

        # Set our desired cash start
        self.cerebro.broker.setcash(1000000.0)

        # Disable cheat on close
        self.cerebro.broker.set_coc(False)

        # Add a FixedSize sizer according to the stake
        self.cerebro.addsizer(bt.sizers.FixedSize, stake=1)

        # Initiate some analysis result
        self.total_return = None
        self.annual_return = None
        self.max_draw_down = None
        self.sharpe_ratio = None
        self.total = None
        self.won_ratio = None

    def add_strategy(self, strategy, *args, **kwargs):
        """add strategy to cerebro."""
        self.cerebro.addstrategy(strategy, *args, **kwargs)

    def add_data(self, data, name=None):
        """add data to cerebro."""
        self.cerebro.adddata(data, name=name)

    def run(self):
        """run the analysis."""
        # Print out the starting conditions
        value = self.cerebro.broker.getvalue()
        logger.info("starting portfolio value: %.2f", value)

        # Run over everything
        result = self.cerebro.run()

        # Print out the final result
        value = self.cerebro.broker.getvalue()
        logger.info("final Portfolio Value: %.2f", value)

        return result

    def show_return(self, result):
        """analyze the return."""
        returns = result[0].analyzers.Returns.get_analysis()
        self.total_return = math.exp(returns["rtot"]) * 100
        self.annual_return = returns["rnorm"] * 100
        logger.info("total return: %.1f%%", self.total_return)
        logger.info("annual return: %.1f%%", self.annual_return)

        years_return = result[0].analyzers.AnnualReturn.get_analysis()
        for year in years_return:
            r = years_return[year] * 100
            logger.info("%d return: %.2f%%", year, r)

    def show_max_draw_down(self, result):
        """analyze the max draw down."""
        draw_down = result[0].analyzers.DrawDown.get_analysis()
        self.max_draw_down = draw_down["max"]["drawdown"]
        logger.info("max draw down: %.1f%%", self.max_draw_down)

    def show_sharpe_ratio(self, result):
        """analyze the sharpe ratio."""
        sharpe = result[0].analyzers.SharpeRatio_A.get_analysis()
        self.sharpe_ratio = sharpe["sharperatio"]
        logger.info("sharpe ratio: %.3f", self.sharpe_ratio)

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

        self.total = trade_analyzer["total"]["total"]
        net = trade_analyzer["pnl"]["net"]["total"]
        gross = trade_analyzer["pnl"]["gross"]["total"]
        comm = gross - net

        won_total = trade_analyzer["won"]["total"]
        self.won_ratio = won_total * 1.0 / self.total
        won_profit_total = trade_analyzer["won"]["pnl"]["total"]
        won_profit_average = trade_analyzer["won"]["pnl"]["average"]

        lost_total = trade_analyzer["lost"]["total"]
        lost_profit_total = trade_analyzer["lost"]["pnl"]["total"]
        lost_profit_average = trade_analyzer["lost"]["pnl"]["average"]

        logger.info(
            "\nnet: %.0f, won: %.0f, lost: %.0f, comm: %.0f",
            net,
            won_profit_total,
            lost_profit_total,
            comm)
        logger.info(
            "\ntotal trade number: %d, won: %d, lost: %d, ratio: %.2f",
            self.total,
            won_total,
            lost_total,
            self.won_ratio)
        logger.info(
            "\nwon profit average: %.0f, lost profit average: %.0f",
            won_profit_average,
            lost_profit_average)

    def plot_figure(self, result):
        """plot the figure."""

        ret = pd.Series(result[0].analyzers.TimeReturn.get_analysis())  #

        # create the canvas
        _, ax1 = pyplot.subplots(figsize=(20, 12), dpi=200)
        ax1.set_title("profit", fontsize=30)
        pyplot.grid(True, linestyle="--")

        ax1.plot(
            (ret + 1).cumprod().index,
            (ret + 1).cumprod().values,
            "r-",
            label="profit")

        pyplot.show()

    def show(self, result, plot=True):
        """show the backtest result."""
        logger.info("\n*************** Overview *************")

        # show the return.
        self.show_return(result)
        # show the max draw down.
        self.show_max_draw_down(result)
        # show the sharpe ratio
        self.show_sharpe_ratio(result)
        # show the trade analyzer
        self.show_trade_analyzer(result)

        # plot the figures.
        if plot:
            self.plot_figure(result)
            self.cerebro.plot()
