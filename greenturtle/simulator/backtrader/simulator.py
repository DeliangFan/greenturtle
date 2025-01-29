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
from greenturtle.analyzers import summary
from greenturtle.util.logging import logging


logger = logging.get_logger()


# pylint: disable=too-many-instance-attributes
class Simulator():

    """Basic analysis class for backtrader."""

    def __init__(self,
                 cash=1000000,
                 commission=0.001,
                 slippage=0.001,
                 plot=False):

        self.plot = plot
        self.summary = summary.Summary()

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
        self.cerebro.broker.setcash(cash)

        # Set short cash
        self.cerebro.broker.set_shortcash(False)

        # Disable cheat on close
        self.cerebro.broker.set_coc(False)

        # Add a FixedSize sizer according to the stake
        self.cerebro.addsizer(bt.sizers.FixedSize, stake=1)

    def add_strategy(self, strategy, *args, **kwargs):
        """add strategy to cerebro."""
        self.cerebro.addstrategy(strategy, *args, **kwargs)

    def add_data(self, data, name=None):
        """add data to cerebro."""
        self.cerebro.adddata(data, name=name)

    def do_simulate(self):
        """perform simulation including run and analysis."""

        result = self.run()

        # analysis the return.
        self.analysis_return(result)

        # analysis position pln
        self.analysis_positions_pnl(result)

        # analysis the max draw down.
        self.analysis_max_draw_down(result)

        # analysis the sharpe ratio
        self.analysis_sharpe_ratio(result)

        # analysis the leverage
        self.analysis_leverage_ratio(result)

        # analysis the trade analyzer
        self.analysis_trade(result)

        # print the result and plot figure
        self.show()

    def run(self):
        """run the cerebro to perform backtesting."""

        # Print out the starting conditions
        value = self.cerebro.broker.getvalue()
        logger.info("starting portfolio value: %.2f", value)

        # Run over everything
        result = self.cerebro.run()

        # Print out the final result
        value = self.cerebro.broker.getvalue()
        logger.info("final Portfolio Value: %.2f", value)

        return result

    def analysis_return(self, result):
        """analysis the return."""
        analysis = result[0].analyzers.Returns.get_analysis()
        total_return = (math.exp(analysis["rtot"]) - 1) * 100
        annual_return = analysis["rnorm"] * 100

        analysis = result[0].analyzers.AnnualReturn.get_analysis()
        year_return = {}
        for year in analysis:
            year_return[year] = analysis[year] * 100

        return_summary = summary.ReturnSummary(
            total_return=total_return,
            annual_return=annual_return,
            year_return=year_return)

        self.summary.return_summary = return_summary

    def analysis_max_draw_down(self, result):
        """analysis the max draw down."""
        analysis = result[0].analyzers.DrawDown.get_analysis()
        max_draw_down = analysis["max"]["drawdown"]

        max_draw_down_summary = summary.MaxDrawDownSummary(
            max_draw_down=max_draw_down)

        self.summary.max_draw_down_summary = max_draw_down_summary

    def analysis_sharpe_ratio(self, result):
        """analysis the sharpe ratio."""
        analysis = result[0].analyzers.SharpeRatio_A.get_analysis()
        sharpe_ratio = analysis["sharperatio"]

        sharpe_ratio_summary = summary.SharpeRatioSummary(
            sharpe_ratio=sharpe_ratio)

        self.summary.sharpe_ratio_summary = sharpe_ratio_summary

    def analysis_leverage_ratio(self, result):
        """analysis the leverage ratio."""
        analysis = result[0].analyzers.GrossLeverage.get_analysis()

        total = 0.0
        for k in analysis:
            total = total + analysis[k]
        leverage_ratio = total / len(analysis)

        leverage_ratio_summary = summary.LeverageRatioSummary(
            leverage_ratio=leverage_ratio)

        self.summary.leverage_ratio_summary = leverage_ratio_summary

    def analysis_trade(self, result):
        """analysis the trade details including profit and lost."""

        analysis = result[0].analyzers.TradeAnalyzer.get_analysis()
        if (
                ("pnl" not in analysis) or
                ("total" not in analysis) or
                ("won" not in analysis) or
                ("lost" not in analysis)
        ):
            return

        net = analysis["pnl"]["net"]["total"]
        gross = analysis["pnl"]["gross"]["total"]
        won = analysis["won"]["pnl"]["total"]
        lost = analysis["lost"]["pnl"]["total"]
        trader_number = analysis["total"]["total"]
        won_trader_number = analysis["won"]["total"]

        trade_summary = summary.TradeSummary(
            net=net,
            gross=gross,
            won=won,
            lost=lost,
            trader_number=trader_number,
            won_trader_number=won_trader_number)

        self.summary.trade_summary = trade_summary

    def analysis_positions_pnl(self, result):
        """analysis profit and lost for all positions."""
        analysis = result[0].analyzers.PositionPNL.get_analysis()

        positions_summary = summary.PositionsPNLSummary(
            positions_pnl=analysis)
        self.summary.positions_pnl_summary = positions_summary

    def show(self):
        """show the backtest result."""

        message = self.summary.to_string()
        logger.info(message)

        # plot the figures.
        if self.plot:
            self.cerebro.plot()
