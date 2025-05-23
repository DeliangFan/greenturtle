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

""" Base strategy class for backtrader which implements some basic interface"""

import abc
import copy
from datetime import date as datetime_date

import backtrader as bt

from greenturtle.constants import types
from greenturtle.data.datafeed import db
from greenturtle.data.datafeed import mock
from greenturtle.data import validation
from greenturtle.util.logging import logging
from greenturtle import exception


logger = logging.get_logger()


class BaseStrategy(bt.Strategy):

    """ base strategy for backtrader framework."""

    # pylint: disable=too-many-instance-attributes, too-many-arguments
    # pylint: disable=too-many-positional-arguments
    def __init__(self,
                 allow_short=False,
                 risk_factor=0.002,
                 atr_period=100,
                 varieties=None,
                 group_risk_factors=None,
                 inference=False,
                 trading_date=datetime_date.today()):

        super().__init__()
        self.allow_short = allow_short
        self.risk_factor = risk_factor
        self.varieties = varieties
        self.group_risk_factors = group_risk_factors
        self.inference = inference
        self.trading_date = trading_date
        self.order = None
        self.bankruptcy = False
        self.portfolio_type = types.PORTFOLIO_TYPE_ATR
        self._init_others(atr_period)

    def _init_others(self, atr_period):
        """init others attributes."""
        self.symbols_data = {}
        self.atrs = {}
        self.names = self.getdatanames()
        for name in self.names:
            data = self.getdatabyname(name)
            self.symbols_data[name] = data
            self.atrs[name] = bt.indicators.ATR(data, period=atr_period)

    def _clear_order(self):
        self.order = None

    def log(self, txt, dt=None):
        """ Logging function fot this strategy."""
        dt = dt or self.datas[0].datetime.date(0)
        iso_time = dt.isoformat()
        logger.info("%s: %s", iso_time, txt)

    def start(self):
        self._clear_order()

    def next(self):
        """
        next function in strategy.
               +--buy_to_open----+  +---sell_to_open--+
               V                 |  |                 V
        + ----------+         +-------+          +------------+
        | long hold |         | Empty |          | short hold |
        +----------+          +-------+          +------------+
              |                ^   ^                  |
              +--sell_to_close-+   +-- buy_to_close ---
        """

        data_date = self.datas[0].datetime.date(0)

        self._validate_all_data()

        # In the inference model, only perform a trade with the same date.
        # TODO(wsfdl), more strict validation for online trading data.
        if self.inference:
            if self.trading_date != data_date:
                logger.info("%s skip trading since not match inference date",
                            data_date)
                return

        if self.order:
            return

        if self.bankruptcy:
            logger.error("%s skip trading due to bankruptcy", data_date)
            return

        if self._check_bankruptcy():
            logger.error("%s skip trading due to bankruptcy", data_date)
            return

        if self.inference and self.broker.get_orders_open():
            logger.warning("%s trading with open order", data_date)

        # 1. get the long and short hold position
        hold = self.get_hold_symbols()
        hold_long = self.get_long_symbols_within_hold()
        hold_short = self.get_short_symbols_within_hold()

        # 2. compute the long and short desired position
        desired_long = self.compute_desired_long_symbols(hold_long, hold)
        desired_short = self.compute_desired_short_symbols(hold_short, hold)
        self._validate_portfolios(desired_long, desired_short)

        # 3. determine if whether need trade or not
        if hold_long == desired_long and hold_short == desired_short:
            return

        self.log("symbols" +
                 f"\nhold long: {sorted(list(hold_long))}" +
                 f"\nhold short: {sorted(list(hold_short))}" +
                 f"\ndesired long: {sorted(list(desired_long))}" +
                 f"\ndesired short: {sorted(list(desired_short))}")

        # 4. get the current portfolios
        current_portfolios = self.get_current_portfolios()

        # 5. compute the desired portfolios with detailed size
        desired_portfolios = self.compute_desired_portfolios(
            desired_long,
            desired_short,
            current_portfolios)

        # 6. execute the orders.
        self.execute(current_portfolios, desired_portfolios)

    def _validate_all_data(self):
        """validate all the data in data feed."""
        for name in self.names:
            data = self.getdatabyname(name)
            self._do_validate_one(data)

    def _is_valid(self, name):
        """is variety data valid."""
        data = self.symbols_data[name]
        if hasattr(data, "valid"):
            return data.valid[0] > 0
        return True

    @staticmethod
    def _do_validate_one(data):
        """valid the single data."""
        validation.validate_price(data.open[0],
                                  data.high[0],
                                  data.low[0],
                                  data.close[0])

    def _check_bankruptcy(self):
        """check if account is bankrupt"""
        total_value = self.broker.get_value()
        cash = self.broker.get_cash()

        if total_value <= 0 and cash <= 0:
            logger.error("bankruptcy, stop backtest!!!")
            self.bankruptcy = True

        return self.bankruptcy

    def _get_name_from_position_key(self, key):
        """get name from position key."""
        if isinstance(key, str):
            return key

        if isinstance(key, db.ContinuousContractDB):
            return key.p.variety

        if isinstance(key, mock.MockPandasData):
            return key.get_name()

        raise ValueError("unknown position key")

    def get_hold_symbols(self):
        """get symbols in hold."""
        symbols = set()
        positions = self.getpositions()

        for key, position in positions.items():
            name = self._get_name_from_position_key(key)
            if position.size > 0 or position.size < 0:
                symbols.add(name)

        return symbols

    def get_long_symbols_within_hold(self):
        """get long symbols in hold."""
        symbols = set()
        positions = self.getpositions()

        for key, position in positions.items():
            name = self._get_name_from_position_key(key)
            if position.size > 0:
                symbols.add(name)

        return symbols

    def get_short_symbols_within_hold(self):
        """get short symbols in hold."""
        symbols = set()
        positions = self.getpositions()

        for key, position in positions.items():
            name = self._get_name_from_position_key(key)
            if position.size < 0:
                symbols.add(name)

        return symbols

    def compute_desired_long_symbols(self, long_hold, hold):
        """compute the desired long symbols"""
        symbols = set()

        for name in self.names:
            if not self._is_valid(name):
                continue

            # 1. for symbol already in position, hold it unless it meet
            # the condition for selling to close.
            if name in long_hold:
                if not self.is_sell_to_close(name):
                    symbols.add(name)

            # 2. for symbol not in position, buy it if it meets the condition
            # for buying to open.
            if name not in hold:
                if self.is_buy_to_open(name):
                    symbols.add(name)

        return symbols

    def compute_desired_short_symbols(self, short_hold, hold):
        """compute the desired short symbols"""
        symbols = set()
        if not self.allow_short:
            return symbols

        for name in self.names:
            if not self._is_valid(name):
                continue

            # 1. for symbol already in position, hold it unless it meet
            # the condition for buying to close.
            if name in short_hold:
                if not self.is_buy_to_close(name):
                    symbols.add(name)
            # 2. for symbol not in position, buy it if it meets the condition
            # for selling to open.
            if name not in hold:
                if self.is_sell_to_open(name):
                    symbols.add(name)

        return symbols

    @abc.abstractmethod
    def is_buy_to_open(self, name):
        """determine whether a position should buy to open or not."""
        raise NotImplementedError

    @abc.abstractmethod
    def is_sell_to_close(self, name):
        """determine whether a position should sell to close or not."""
        raise NotImplementedError

    @abc.abstractmethod
    def is_sell_to_open(self, name):
        """determine whether a position should sell to open or not."""
        raise NotImplementedError

    @abc.abstractmethod
    def is_buy_to_close(self, name):
        """determine whether a position should buy to close or not."""
        raise NotImplementedError

    def _validate_portfolios(self, desired_long, desired_short):
        """validate the portfolio symbols."""

        if desired_short is None:
            desired_short = set()

        if desired_long is None:
            desired_long = set()

        if desired_short.intersection(desired_long):
            raise exception.SymbolUnexpectedIntersectionError()

        if not self.allow_short and len(desired_short) > 0:
            raise exception.SymbolUnexpectedIntersectionError()

    def get_current_portfolios(self):
        """get current portfolios within hold."""

        portfolios = {}
        positions = self.getpositions()

        for key, position in positions.items():
            name = self._get_name_from_position_key(key)
            if position.size != 0:
                # pylint: disable=protected-access
                portfolios[name] = position.size

        return portfolios

    def _compute_single_risk_with_size(self, name, size):
        """compute real risk according to the size."""
        # get the mult parameter
        data = self.symbols_data[name]
        commissioninfo = self.broker.getcommissioninfo(data)
        mult = commissioninfo.p.mult

        # get the atr
        atr = self.atrs[name]

        # get the total value
        total_value = self.broker.get_value()

        # compute the risk
        risk = abs(size) * mult * atr[0] / total_value

        return risk

    def _compute_single_portfolio_by_atr(self, name):
        """compute portfolio by atr.

        formula: size = risk_factor * value / atr / mult
        """
        # get the mult parameter
        data = self.symbols_data[name]
        commissioninfo = self.broker.getcommissioninfo(data)
        mult = commissioninfo.p.mult

        # get the atr
        atr = self.atrs[name]

        # get the total value
        total_value = self.broker.get_value()

        # compute the size
        size = int(self.risk_factor * total_value / (atr[0] * mult))

        return size

    def _compute_single_portfolio(self, name):
        """compute single portfolio."""

        if self.portfolio_type == types.PORTFOLIO_TYPE_ATR:
            size = self._compute_single_portfolio_by_atr(name)
        else:
            raise NotImplementedError

        return size

    def _get_group_by_name(self, name):
        """get group name by variety name"""
        for group_name, group_value in self.varieties.items():
            for variety in group_value:
                if variety == name:
                    return group_name
        return None

    # pylint: disable = too-many-branches, too-many-locals, too-many-statements
    def adjust_portfolio_by_group(self,
                                  desired_portfolios,
                                  current_portfolios):
        """refine portfolio by group."""
        if self.group_risk_factors is None:
            return desired_portfolios

        adjust_desired_portfolios = copy.deepcopy(desired_portfolios)

        # 1. calculate the group risk
        group_risk_dict = {}
        # calculate the group risk
        for name, size in desired_portfolios.items():
            # get group name
            group_name = self._get_group_by_name(name)
            # raise exception if group not found.
            if group_name is None:
                raise exception.GroupNameNotFound

            # accumulate group risk in the desired portfolio
            risk = self._compute_single_risk_with_size(name, size)
            if group_name in group_risk_dict:
                group_risk_dict[group_name] += risk
            else:
                group_risk_dict[group_name] = risk

        # 2. adjust the size according to current group risk and the
        # limitation of the group risk.
        adjust_group_risk_dict = {}
        for name, size in desired_portfolios.items():
            # get the group name, group risk and limit
            group_name = self._get_group_by_name(name)
            group_risk = group_risk_dict[group_name]
            group_limit = self.group_risk_factors[group_name]

            # if the group risk it more than limit, then adjust the size
            if group_risk > group_limit:
                size = int(size * group_limit / group_risk)

            # set the value to adjust_desired_portfolios
            adjust_desired_portfolios[name] = size

            # accumulate the adjust group risk in the desired portfolio
            adjust_risk = self._compute_single_risk_with_size(name, size)
            if group_name in adjust_group_risk_dict:
                adjust_group_risk_dict[group_name] += adjust_risk
            else:
                adjust_group_risk_dict[group_name] = adjust_risk

        # 3. refine the desired_portfolios with low startup value
        # 3.1 refine the size with current and desired hold position
        for name, current_size in current_portfolios.items():
            # skip if it not in the desired and adjust portfolios
            if name not in desired_portfolios:
                continue
            if name not in adjust_desired_portfolios:
                continue

            # refine the 0 adjust size
            desired_size = desired_portfolios[name]
            adjust_size = adjust_desired_portfolios[name]
            if desired_size != 0 and adjust_size == 0 and current_size != 0:
                adjust_size = 1 if desired_size > 0 else -1
            else:
                continue

            # compute the risk and prepare the group risk parameters
            risk = self._compute_single_risk_with_size(name, adjust_size)
            group_name = self._get_group_by_name(name)
            adjust_group_risk = adjust_group_risk_dict[group_name]
            group_limit = self.group_risk_factors[group_name]

            # check if respect to the group risk limitation
            if risk + adjust_group_risk > group_limit:
                continue

            # meet the requirement and refine the risk and size value
            adjust_group_risk_dict[group_name] += risk
            adjust_desired_portfolios[name] = adjust_size

        # 3.2 refine the size with desired hold position
        for name, desired_size in desired_portfolios.items():
            # skip if it not in the adjust portfolios
            if name not in adjust_desired_portfolios:
                continue

            # refine the 0 adjust size
            adjust_size = adjust_desired_portfolios[name]
            if desired_size != 0 and adjust_size == 0:
                adjust_size = 1 if desired_size > 0 else -1
            else:
                continue

            # compute the risk and prepare the group risk parameters
            risk = self._compute_single_risk_with_size(name, adjust_size)
            group_name = self._get_group_by_name(name)
            adjust_group_risk = adjust_group_risk_dict[group_name]
            group_limit = self.group_risk_factors[group_name]

            # check if respect to the group risk limitation
            if risk + adjust_group_risk > group_limit:
                continue

            # meet the requirement and refine the risk and size value
            adjust_group_risk_dict[group_name] += risk
            adjust_desired_portfolios[name] = adjust_size

        return adjust_desired_portfolios

    def compute_desired_portfolios(self,
                                   long_desired,
                                   short_desired,
                                   current_portfolios):
        """compute the desired portfolio."""

        desired_portfolios = {}
        if len(long_desired) + len(short_desired) == 0:
            return desired_portfolios

        for name in self.names:
            size = self._compute_single_portfolio(name)

            if name in long_desired:
                desired_portfolios[name] = size
            if name in short_desired:
                desired_portfolios[name] = -size

        desired_portfolios = self.adjust_portfolio_by_group(
            desired_portfolios, current_portfolios)

        return desired_portfolios

    def _filter_portfolios_by_valid(self, portfolios):
        """filter the portfolios by data valid."""
        filtered = {}
        for k, v in portfolios.items():
            if self._is_valid(k):
                filtered[k] = v
            else:
                logger.warning("%s skip trading hold %s since invalid data",
                               self.datas[0].datetime.date(0), k)
        return filtered

    def execute(self, current_portfolios, desired_portfolios):
        """execute the orders with the following rule."""

        # 1. filter the portfolios with invalid data
        current_portfolios = self._filter_portfolios_by_valid(
            current_portfolios)

        # 2. sell the unwanted symbols.
        for name in current_portfolios:
            if name not in desired_portfolios:
                self.order_target_size_with_log(name, 0)

        # 3. trade the symbols both in current and desired portfolios
        # 3.1 trade the symbols to get more available cash
        for name, current_size in current_portfolios.items():
            if name in desired_portfolios:
                desired_size = desired_portfolios[name]
                if abs(current_size) > abs(desired_size):
                    self.order_target_size_with_log(name, desired_size)

        # 3.2 trade other symbols both in current and desired portfolios
        for name, current_size in current_portfolios.items():
            if name in desired_portfolios:
                desired_size = desired_portfolios[name]
                if current_size == desired_size:
                    continue
                if abs(current_size) <= abs(desired_size):
                    self.order_target_size_with_log(name, desired_size)

        # 4. trade the new open symbols.
        for name in desired_portfolios:
            if name not in current_portfolios:
                desired_size = desired_portfolios[name]
                if desired_size != 0:
                    self.order_target_size_with_log(name, desired_size)

    def order_target_percent_with_log(self, data=None, target=0.0):
        """
        Order the target percent with loging the price.

        In most case, the strategy computing the signal with close price, and
        here is to log the close price.
        """
        if isinstance(data, str):
            data = self.getdatabyname(data)
        elif data is None:
            data = self.data

        # pylint: disable=protected-access
        name = data._name
        close = data.close[0]
        self.log(f"try to order {name} {target*100:.3f}%" +
                 f" with expected price {close:.3f}")

        self.order_target_percent(data=data, target=target)

    def order_target_size_with_log(self, data=None, size=0):
        """
        Order the target size with loging the price.

        In most case, the strategy computing the signal with close price, and
        here is to log the close price.
        """

        if isinstance(data, str):
            data = self.getdatabyname(data)
        elif data is None:
            data = self.data

        # pylint: disable=protected-access
        name = data._name
        close = data.close[0]
        position = self.getpositionbyname(name)
        original_size = 0 if position is None else position.size

        self.log(f"try to adjust {name} size from {original_size} to" +
                 f" {size} with price {close:.3f}")

        # desired is the same as target to pass to tq broker.
        kwargs = {types.DESIRED_SIZE: size, types.VARIETY: name}
        self.order_target_size(data=data, target=size, **kwargs)

    def notify_order(self, order):
        """
        notify order response the order according to the status of the order
        and log the order.
        """

        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:

            # order information
            # pylint: disable=protected-access
            name, price = order.data._name, order.executed.price
            size, comm = order.executed.size, order.executed.comm
            value = order.executed.value

            # additional information for future
            commissioninfo = self.broker.getcommissioninfo(order.data)
            multiplier = commissioninfo.p.mult
            nominal_value = size * price * multiplier
            stock_like = commissioninfo.stocklike

            # logging the order
            msg = f"name: {name}, price: {price:.3f}, " + \
                  f"size: {size:.0f}, comm: {comm:.2f}"

            if order.isbuy():
                msg = "BUY EXECUTED, " + msg
            elif order.issell():
                msg = "SELL EXECUTED, " + msg

            if stock_like:
                msg = msg + f", value: {value}"
            else:
                msg = msg + f", margin: {value}"
                msg = msg + f", nominal value: {nominal_value:.2f}"

            # logging the order
            self.log(msg)

            # logging the total value and order after executed
            total_value = self.broker.get_value()
            cash = self.broker.getcash()
            msg = f"after execute total value: {total_value:.0f}, " + \
                  f"cash: {cash:.0f}"
            self.log(msg)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self._clear_order()
