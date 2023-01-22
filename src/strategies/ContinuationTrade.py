"""Implement an implementation of Strategy for a continuation trade.

Classes
----------
    ContinuationTrade:
        Implement the buy and sell logic of a continuation trade.
"""
from dataclasses import dataclass
import logging

import numpy as np
import pandas as pd

from MarketStructure import MarketStructure
from Strategy import Strategy


class ContinuationTrade(Strategy):
    """Implements the logical rules for a trend reversal trade triggered by an
    initial market structure break.

    ...

    Methods
    -------
    next_candle_setup(row: pd.Series) -> None:
        Initializes the strategy by iterating through historical data without
        executing trades.
    next_candle_trade(row: pd.Series) -> None:
        Checks for valid trade set ups with new live data and execute live
        trades.
    """

    def __init__(self, ms: MarketStructure, asset: dataclass):
        """
        Parameters
        ----------
        ec : RESTClient
            Exchange client to interact with the exchange.
        ms : MarketStructure
            Represent the market structure of the asset.
        asset : dict
            Asset to trade.
        live : bool, optional
            Whether the strategy is live or not, by default False
        message : bool, optional
            Whether to send messages to Telegram, by default True
        """

        super().__init__(ms, asset)
        self._risk_reward = asset.risk_reward

    def next_candle_setup(self, row: pd.Series) -> None:
        """Activates trade triggers and sets stop losses.

        Parameters
        ----------
        row : pd.Series
            Row of live data.
        """

        trend, msb, continuation, stay_in_range = self.ms.next_candle(row)
        self.close = row['close']

        if continuation and trend:
            self._entry = 0.66*self.ms.prev_low[0] + 0.33*self.ms.prev_high[0]
            self._stop_loss = self.ms.prev_low[0]
            self._long_trigger = True
        elif continuation and (not trend):
            self._entry = 0.66*self.ms.prev_high[0] + 0.33*self.ms.prev_low[0]
            self._stop_loss = self.ms.prev_high[0]
            self._short_trigger = True

        self.position_size.append(self._position)
        self.equity_curve = np.append(self.equity_curve, self.equity)

    def next_candle_trade(self, row: pd.Series) -> None:
        """Enters trade after triggered and follows through until trade exit.

        Parameters
        ----------
        row : pd.Series
            Row of live data.
        """

        # Entry Long
        if self._long_trigger:
            price = row['close']
            if price <= self.ms.prev_low[0]:
                self._long_trigger = False
            elif price >= self.ms.prev_high[0] and not self.ms.continuation:
                self._long_trigger = False
            else:
                if price <= self._entry:
                    target = self.ms.prev_high[0]
                    risk = price - self._stop_loss
                    reward_risk = (target - price)/risk
                    if reward_risk >= self._risk_reward:
                        self._target = target
                        self._long(price, risk/price)
                        self.num_trades += 1
                        self._long_position = True
                        self._long_trigger = False

        if self._long_position:
            price = row['close']
            if price > self._target:
                self._close_long_trade(price)
                logging.info('Take Profit on Long Position')
                self._long_position = False
                self.wins += 1
                self.win_rate = self.wins/self.num_trades
            if price < self._stop_loss:
                self._close_long_trade(price)
                logging.info('Stop Loss Hit on Long Position')
                self._long_position = False

        if self._short_trigger:
            price = row['close']
            if price >= self.ms.prev_high[0]:
                self._short_trigger = False
            elif price <= self.ms.prev_low[0] and not self.ms.continuation:
                self._short_trigger = False
            else:
                if price >= self._entry:
                    risk = self._stop_loss - price
                    reward_risk = (price - self.ms.prev_low[0])/risk
                    if reward_risk >= self._risk_reward:
                        self._target = self.ms.prev_low[0]
                        self._short(price, risk/price)
                        self.num_trades += 1
                        self._short_position = True
                        self._short_trigger = False

        if self._short_position:
            price = row['close']
            if price < self._target:
                self._close_short_trade(price)
                logging.info('Take Profit on Short Position')
                self._short_position = False
                self.wins += 1
                self.win_rate = self.wins/self.num_trades
            if price > self._stop_loss:
                self._close_short_trade(price)
                logging.info('Stop Loss Hit on Short Position')
                self._short_position = False
