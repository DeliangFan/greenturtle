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
from backtrader import analyzers

from greenturtle.analyzers.backtrader import position_pnl
from greenturtle.util import panda_util
from greenturtle.util.logging import logging


logger = logging.get_logger()


def do_simulate(datas,
                strategy,
                *strategy_args,
                plot=False,
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


# pylint: disable=too-many-instance-attributes
class Simulator():

    """Basic analysis class for backtrader."""

    def __init__(self, commission=0.001, slippage=0.001):
        self.cerebro = bt.Cerebro()

        # add analyzer
        self.cerebro.addanalyzer(
            analyzers.AnnualReturn,
            _name="AnnualReturn")
        self.cerebro.addanalyzer(
            analyzers.TimeReturn,
            _name="TimeReturn")
        self.cerebro.addanalyzer(
            analyzers.Returns,
            _name="Returns",
            tann=252)
        self.cerebro.addanalyzer(
            analyzers.DrawDown,
            _name="DrawDown")
        self.cerebro.addanalyzer(
            analyzers.SharpeRatio_A,
            _name="SharpeRatio_A")
        self.cerebro.addanalyzer(
            analyzers.TradeAnalyzer,
            _name="TradeAnalyzer")
        self.cerebro.addanalyzer(
            analyzers.GrossLeverage,
            _name="GrossLeverage")
        self.cerebro.addanalyzer(
            position_pnl.PositionPNL,
            _name="PositionPNL")

        # Set the commission
        self.cerebro.broker.setcommission(commission=commission)
        self.cerebro.broker.set_slippage_perc(perc=slippage)

        # Set our desired cash start
        self.cerebro.broker.setcash(100000000.0)

        # Set short cash
        self.cerebro.broker.set_shortcash(False)

        # Disable cheat on close
        self.cerebro.broker.set_coc(False)

        # Add a FixedSize sizer according to the stake
        self.cerebro.addsizer(bt.sizers.FixedSize, stake=1)

        # Initiate some analysis result
        self.total_return = None
        self.annual_return = None
        self.leverage = None
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
        analysis = result[0].analyzers.Returns.get_analysis()
        self.total_return = math.exp(analysis["rtot"]) * 100
        self.annual_return = analysis["rnorm"] * 100
        logger.info("total return: %.1f%%", self.total_return)
        logger.info("annual return: %.1f%%", self.annual_return)

        analysis = result[0].analyzers.AnnualReturn.get_analysis()
        for year in analysis:
            r = analysis[year] * 100
            logger.info("%d return: %.2f%%", year, r)

    def show_max_draw_down(self, result):
        """analyze the max draw down."""
        analysis = result[0].analyzers.DrawDown.get_analysis()
        self.max_draw_down = analysis["max"]["drawdown"]
        logger.info("max draw down: %.1f%%", self.max_draw_down)

    def show_sharpe_ratio(self, result):
        """analyze the sharpe ratio."""
        analysis = result[0].analyzers.SharpeRatio_A.get_analysis()
        self.sharpe_ratio = analysis["sharperatio"]
        logger.info("sharpe ratio: %.3f", self.sharpe_ratio)

    def show_leverage(self, result):
        """analyze the leverage."""
        analysis = result[0].analyzers.GrossLeverage.get_analysis()
        total = 0.0
        for k in analysis:
            total = total + analysis[k]
        self.leverage = total / len(analysis)
        logger.info("leverage ratio: %.2f", self.leverage)

    def show_trade_analyzer(self, result):
        """analyze the trade."""

        analysis = result[0].analyzers.TradeAnalyzer.get_analysis()

        if (
                ("pnl" not in analysis) or
                ("total" not in analysis) or
                ("won" not in analysis) or
                ("lost" not in analysis)
        ):
            return

        self.total = analysis["total"]["total"]
        net = analysis["pnl"]["net"]["total"]
        gross = analysis["pnl"]["gross"]["total"]
        comm = gross - net

        won_total = analysis["won"]["total"]
        self.won_ratio = won_total * 1.0 / self.total
        won_profit_total = analysis["won"]["pnl"]["total"]
        won_profit_average = analysis["won"]["pnl"]["average"]

        lost_total = analysis["lost"]["total"]
        lost_profit_total = analysis["lost"]["pnl"]["total"]
        lost_profit_average = analysis["lost"]["pnl"]["average"]

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

    def show_position_pnl(self, result):
        """show profit and lost for all positions."""

        message = ""
        analysis = result[0].analyzers.PositionPNL.get_analysis()

        for name in analysis:
            pln = analysis[name]
            net = pln["net"]
            profit = pln["profit"]
            lost = pln["lost"]
            comm = pln["gross"] - pln["net"]
            count = pln["count"]
            message += f"\n{name}, net: {net:.0f}, profit: {profit:.0f}, " + \
                f"lost: {lost:.0f}, comm: {comm:.0f}, trader number: {count}"

        logger.info(message)

    def show(self, result, plot=True):
        """show the backtest result."""
        logger.info("\n*************** Overview *************")

        # show the return.
        self.show_return(result)
        # show position pln
        self.show_position_pnl(result)
        # show the max draw down.
        self.show_max_draw_down(result)
        # show the sharpe ratio
        self.show_sharpe_ratio(result)
        # show the leverage
        self.show_leverage(result)
        # show the trade analyzer
        self.show_trade_analyzer(result)

        # plot the figures.
        if plot:
            self.cerebro.plot()
