"""Implement classes to represent assets.

Implements dictionaries representing assets and their respective risk
parameters for trading.

Classes
----------
    Implements a dataclass Asset holding relevant information for one asset.
"""

from dataclasses import dataclass
from datetime import datetime

import numpy as np

from MarketStructure import MarketStructure


class Asset:
    """Represents an Asset Class to be traded.

    ...

    Attributes
    ----------
    market_name : str
        The ticker of the asset to be traded.
    ath : tuple
        A past all time high of the asset.
    prev_low : tuple
        Low preceding the all time high.
    start_time : datetime
        The time at which the historical data starts.
    initial_equity : float
        The initial equity to be used for trading.
    timeframe : str
        The timeframe of the historical data.
    decimals : int
        The maximum number of decimals allowed for the asset.
    """
    def __init__(self, ticker: str, ath: tuple, prev_low: tuple,
                 start_time: datetime, decimals: int):
        self.ticker = ticker
        self.ath = ath
        self.prev_low = prev_low
        self.start_time = start_time
        self.decimals = decimals
        self.ms = MarketStructure(ath, prev_low, ath, prev_low)
        # listing: datetime
        # exchange: str


@dataclass
class Params:
    risk: float
    reward_risk: float
    leverage: float
    timeframe: str = '1h'


@dataclass
class TradeData:
    exchange_fees: float
    num_trades: float = 0.
    win_rate: float = 0.
    position: float = 0.
    wins: int = 0
    long_trigger: bool = False
    long_position: bool = False
    short_trigger: bool = False
    short_position: bool = False
    entry: float = None
    stop_loss: float = None
    target: float = None
    close: float = None
    equity_curve: np.array = np.array([100.0])
    equity: float = 100.0

    @property
    def mark_to_market(self) -> float:
        """Returns the current equity value of the strategy.

        Returns
        -------
        float
            The current equity value of the strategy.
        """

        if self.long_position or self.short_position:
            return (self.position*self.close) + self.equity
        else:
            return self.equity_curve[-1]
    

btc = Asset('BTCBUSD', (58434.0, '2021-02-21 19:00:00+00:00'),
            (57465.0, '2021-02-21 18:00:00+00:00'),
            datetime(2021, 2, 21, 20, 0, 0, 0), 3)

eth = Asset('ETHBUSD', (4875.4, '2021-11-10 14:00:00+00:00'),
             (4697.8, '2021-11-10 12:00:00+00:00'),
             datetime(2021, 11, 10, 15, 0, 0, 0), 3)

sol = Asset('SOLBUSD', (261.5175, '2021-11-06 21:00:00+00:00'),
            (252.49, '2021-11-06 20:00:00+00:00'),
            datetime(2021, 11, 6, 22, 0, 0, 0), 0)

bnb = Asset('BNBBUSD', (693.775, '2021-05-10 06:00:00+00:00'),
            (671.355, '2021-05-10 05:00:00+00:00'),
            datetime(2021, 5, 10, 7, 0, 0, 0), 2)

doge = Asset('DOGEBUSD', (0.744998, '2021-05-08 04:00:00+00:00'),
             (0.6674, '2021-05-08 00:00:00+00:00'),
             datetime(2021, 5, 8, 5, 0, 0, 0), 0)

coins = [btc, eth, sol, bnb, doge]
