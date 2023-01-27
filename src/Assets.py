"""Implement classes to represent assets and strategies.

Implements classes representing assets and their respective risk
parameters for trading.

Classes
----------
Asset:
    Implement a dataclass Asset holding relevant information for one asset.
Params:
    Implement a dataclass Params holding a set of parameters for one strategy.
TradeData:
    Implement a dataclass TradeData holding relevant information for one trade
    for one set of parameters.
"""

from dataclasses import dataclass

import numpy as np

from src.MarketStructure import MarketStructure


@dataclass
class Asset:
    """Represent an Asset Class to be traded.

    ...

    Attributes
    ----------
    ticker : str
        The ticker of the asset to be traded.
        The timeframe of the historical data.
    decimals : int
        The maximum number of decimals allowed for the asset.
    ms : MarketStructure
        The current market structure of the asset.
    """

    ticker: str
    decimals: int
    ms: MarketStructure


@dataclass
class Params:
    """Represent the parameters for a trading strategy.

    ...

    Attributes
    ----------
    risk : float
        The percentage of the portfolio at risk per trade.
    reward_risk : float
        The reward to risk ratio of the strategy.
    leverage : float
        The maximal leverage of the strategy.
    timeframe : str
        The timeframe of the historical data.
    """

    risk: float
    reward_risk: float
    leverage: float
    timeframe: str = '1h'


@dataclass
class TradeData:
    """Represent the data of a trade.

    ...

    Attributes
    ----------
    exchange_fees : float
        The exchange fees for the trade.
    entry : float
        The entry price of the trade.
    stop_loss : float
        The stop loss price of the trade.
    target : float
        The target price of the trade.
    close : float
        The close price of the trade.
    num_trades : float
        The number of trades executed.
    wins : int
        The number of winning trades.
    win_rate : float
        The win rate of the strategy.
    position : float
        The position size of the current trade.
    long_trigger : bool
        True if the current setup justifies a long trade.
    long_position : bool
        True if the strategy is currently in an active long trade.
    short_trigger : bool
        True if the current setup justifies a short trade.
    short_position : bool
        True if the strategy is currently in an active short trade.
    equity_curve : np.array
        The equity curve of the strategy.
    equity : float
        The current equity value of the strategy.
    """

    exchange_fees: float
    entry: float = None
    stop_loss: float = None
    target: float = None
    close: float = None
    num_trades: float = 0.
    wins: int = 0
    win_rate: float = 0.
    position: float = 0.
    long_trigger: bool = False
    long_position: bool = False
    short_trigger: bool = False
    short_position: bool = False
    equity_curve: np.array = np.array([100.0])
    equity: float = 100.0

    @property
    def mark_to_market(self) -> float:
        """Returns the current equity value of the strategy.

        Returns
        -------
        float
            The current equity value of the strategy marked to market.
        """

        if self.long_position or self.short_position:
            return (self.position*self.close) + self.equity
        else:
            return self.equity_curve[-1]
