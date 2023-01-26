"""Implement an implementation of Strategy for a continuation trade.

Classes
----------
    ContinuationTrade:
        Implement the buy and sell logic of a continuation trade.
"""
import logging

import numpy as np
import pandas as pd

from Assets import Asset, Params, TradeData
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

    def __init__(self):
        super().__init__()

    def next_candle_setup(self, asset: Asset,
                          trade_data: TradeData, row: pd.Series) -> None:
        """Activates trade triggers and sets stop losses.

        Parameters
        ----------
        row : pd.Series
            Row of live data.
        """

        trend, msb, continuation, stay_in_range = asset.ms.next_candle(row)

        if continuation and trend:
            trade_data.entry = 0.66*asset.ms.prev_low[0] + 0.33*asset.ms.prev_high[0]
            trade_data.stop_loss = asset.ms.prev_low[0]
            trade_data.long_trigger = True
        elif continuation and (not trend):
            trade_data.entry = 0.66*asset.ms.prev_high[0] + 0.33*asset.ms.prev_low[0]
            trade_data.stop_loss = asset.ms.prev_high[0]
            trade_data.short_trigger = True

        trade_data.close = row['close']
        trade_data.equity_curve = np.append(trade_data.equity_curve,
                                            trade_data.mark_to_market)

    def next_candle_trade(self, asset: Asset, params: Params,
                          trade_data: TradeData, row: pd.Series) -> None:
        """Enters trade after triggered and follows through until trade exit.

        Parameters
        ----------
        row : pd.Series
            Row of live data.
        """

        # Entry Long
        if trade_data.long_trigger:
            price = row['close']
            if price <= asset.ms.prev_low[0]:
                trade_data.long_trigger = False
            elif price >= asset.ms.prev_high[0] \
                 and not asset.ms.continuation:
                trade_data.long_trigger = False
            else:
                if price <= trade_data.entry:
                    target = asset.ms.prev_high[0]
                    risk = price - trade_data.stop_loss
                    reward_risk = (target - price)/risk
                    if reward_risk >= params.reward_risk:
                        trade_data.target = target
                        self._long(price, risk/price, asset, params,
                                   trade_data)
                        trade_data.num_trades += 1
                        trade_data.long_position = True
                        trade_data.long_trigger = False

        if trade_data.long_position:
            price = row['close']
            if price > trade_data.target:
                self._close_long_trade(price, trade_data)
                logging.info('Take Profit on Long Position')
                trade_data.long_position = False
                trade_data.wins += 1
                trade_data.win_rate = trade_data.wins/trade_data.num_trades
            if price < trade_data.stop_loss:
                self._close_long_trade(price, trade_data)
                logging.info('Stop Loss Hit on Long Position')
                trade_data.long_position = False

        if trade_data.short_trigger:
            price = row['close']
            if price >= asset.ms.prev_high[0]:
                trade_data.short_trigger = False
            elif price <= asset.ms.prev_low[0] and not asset.ms.continuation:
                trade_data.short_trigger = False
            else:
                if price >= trade_data.entry:
                    risk = trade_data.stop_loss - price
                    reward_risk = (price - asset.ms.prev_low[0])/risk
                    if reward_risk >= params.reward_risk:
                        trade_data.target = asset.ms.prev_low[0]
                        self._short(price, risk/price, asset, params,
                                    trade_data)
                        trade_data.num_trades += 1
                        trade_data.short_position = True
                        trade_data.short_trigger = False

        if trade_data.short_position:
            price = row['close']
            if price < trade_data.target:
                self._close_short_trade(price, trade_data)
                logging.info('Take Profit on Short Position')
                trade_data.short_position = False
                trade_data.wins += 1
                trade_data.win_rate = trade_data.wins/trade_data.num_trades
            if price > trade_data.stop_loss:
                self._close_short_trade(price, trade_data)
                logging.info('Stop Loss Hit on Short Position')
                trade_data.short_position = False
