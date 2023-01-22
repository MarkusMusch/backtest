"""Implement an abstract class as a template for particular strategies.

Classes
----------
    Strategy:
        Implements generic properties of strategies that are
        common amongst all particular trading strategies
        such as buying and selling.
"""

from abc import ABC, abstractmethod

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from dataclasses import dataclass

from MarketStructure import MarketStructure


class Strategy(ABC):
    """Implements generic functions of trades that are common amongst all
    particular trading strategies such as buying and selling.

    ...

    Attributes
    ----------
    ms : MarketStructure
        MarketStructure object representing the market structure.
    equity_curve : np.array
        The equity curve of the strategy.
    position_size : list
        The size of the position at each time step.
    num_trades : int
        The number of trades executed.
    wins : int
        The number of winning trades.
    win_rate : float
        The win rate of the strategy.

    Methods
    -------
    equity -> float:
        Returns the current equity of the strategy.
    plot_equity() -> None:
        Plots the equity curve of the strategy.
    plot_position_size() -> None:
        Plots the position size of the strategy.
    """

    def __init__(self, ms: MarketStructure, asset: dataclass):
        """
        Parameters
        ----------
        ms : MarketStructure
            MarketStructure object representing the market structure.
        asset : dict
            Dictionary of asset information.
        """

        self.ms = ms
        self.timeframe = asset.timeframe
        self.equity_curve = np.array([asset.initial_equity])
        self.position_size = [0]
        self.num_trades = 0
        self.wins = 0
        self.win_rate = 0
        self._strat_name = asset.strategy_name
        self._position = 0
        self._long_trigger = False
        self._long_position = False
        self._short_trigger = False
        self._short_position = False
        self._entry = None
        self._stop_loss = None
        self._target = None
        self._asset = asset
        self._equity = asset.initial_equity

    @abstractmethod
    def next_candle_setup(self, row: pd.Series) -> None:
        """Initializes the strategy by iterating through historical data
        without executing trades."""

        pass

    @abstractmethod
    def next_candle_trade(self, row: pd.Series) -> None:
        """Checks for valid trade set ups with new live data and execute
        live trades."""

        pass

    @property
    def equity(self) -> float:
        """Returns the current equity value of the strategy.

        Returns
        -------
        float
            The current equity value of the strategy.
        """

        if self._long_position or self._short_position:
            return (self._position*self.close) + self._equity
        else:
            return self._equity

    def plot_equity_curve(self) -> None:
        """Plots the equity curve of the strategy."""

        plt.plot(self.equity_curve)
        plt.show()

    def plot_position_size(self) -> None:
        """Plots the position size of the strategy over time."""

        plt.plot(self._position_size)
        plt.show()

    def _long(self, price: float, risk: float) -> None:
        """Enters a long trade.

        Parameters
        ----------
        price : float
            The price at which to buy the asset.
        risk : float
            The risk per trade.
        """

        trade_size = min(self._asset.max_leverage*self._equity,
                         (self._asset.max_risk/risk) * self._equity)
        coins = round(trade_size/price, self._asset.decimals)
        self._position += coins
        self._equity -= coins*price # (1.+self.ec.taker_fees_USD_futures) \
#            * coins*price

    def _short(self, price: float, risk: float) -> None:
        """Enters a short trade.

        Parameters
        ----------
        price : float
            The price at which to sell the asset.
        risk : float
            The risk per trade.
        """

        trade_size = min(self._asset.max_leverage*self._equity,
                         (self._asset.max_risk/risk) * self._equity)
        coins = round(trade_size/price, self._asset.decimals)
        self._position -= coins
        self._equity += coins*price # (1.-self.ec.taker_fees_USD_futures) * coins*price

    def _close_long_trade(self, price: float) -> None:
        """Closes an open long or short positoin.

        Parameters
        ----------
        price : float
            The price at which to close the position.
        """

        # coins = self._position
        cash = self._position*price
        self._equity += cash # (1.-self.ec.taker_fees_USD_futures) * cash
        self._position = 0

    def _close_short_trade(self, price: float) -> None:
        """Closes an open long or short positoin.

        Parameters
        ----------
        price : float
            The price at which to close the position.
        """

        # coins = self._position
        cash = self._position*price
        self._equity += cash # (1.-self.ec.taker_fees_USD_futures) * cash
        self._position = 0
