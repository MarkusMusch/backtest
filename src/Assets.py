"""Implement classes to represent assets.

Implements dictionaries representing assets and their respective risk
parameters for trading.

Classes
----------
    Implements a dataclass Asset holding relevant information for one asset.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from strategies.ContinuationTrade import ContinuationTrade
from strategies.ReversalTrade import ReversalTrade
from Strategy import Strategy
from strategies.TwoTFContinuationTrade import TwoTFContinuationTrade


class Timeframes(Enum):
    #FIVE_MINUTES = '5m'
    #FIFTEEN_MINUTES = '15m'
    #THIRTY_MINUTES = '30m'
    ONE_HOUR = '1h'
    FOUR_HOURS = '4h'
    ONE_DAY = '1d'

@dataclass
class Params:
    risk: float
    reward_risk: float
    leverage: float

@dataclass
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

    ticker: str
    ath: tuple
    prev_low: tuple
    start_time: datetime
    initial_equity: float
    timeframe: str
    decimals: int


btc_cont_1h_5m = Asset('BTCBUSD', (58434.0, '2021-02-21 19:00:00+00:00'),
                       (57465.0, '2021-02-21 18:00:00+00:00'),
                       datetime(2021, 2, 21, 20, 0, 0, 0), 100,
                       Timeframes.ONE_HOUR.value, 3)

eth_cont_1h_5m = Asset('ETHBUSD', (4875.4, '2021-11-10 14:00:00+00:00'),
                       (4697.8, '2021-11-10 12:00:00+00:00'),
                       datetime(2021, 11, 10, 15, 0, 0, 0), 100,
                       Timeframes.ONE_HOUR.value, 3)

sol_cont_1h_5m = Asset('SOLBUSD', (261.5175, '2021-11-06 21:00:00+00:00'),
                       (252.49, '2021-11-06 20:00:00+00:00'),
                       datetime(2021, 11, 6, 22, 0, 0, 0), 100,
                       Timeframes.ONE_HOUR.value, 0)

bnb_cont_1h_5m = Asset('BNBBUSD', (693.775, '2021-05-10 06:00:00+00:00'),
                       (671.355, '2021-05-10 05:00:00+00:00'),
                       datetime(2021, 5, 10, 7, 0, 0, 0), 100,
                       Timeframes.ONE_HOUR.value, 2)

doge_cont_1h_5m = Asset('DOGEBUSD', (0.744998, '2021-05-08 04:00:00+00:00'),
                        (0.6674, '2021-05-08 00:00:00+00:00'),
                        datetime(2021, 5, 8, 5, 0, 0, 0), 100,
                        Timeframes.ONE_HOUR.value, 0)

btc_cont_1h = Asset('BTCBUSD',
                    (58434.0, '2021-02-21 19:00:00+00:00'),
                    (57465.0, '2021-02-21 18:00:00+00:00'),
                    datetime(2021, 2, 21, 20, 0, 0, 0), 100,
                    Timeframes.ONE_HOUR.value, 3)

btc_cont_4h = Asset('BTCBUSD',
                    (58434.0, '2021-02-21 19:00:00+00:00'),
                    (57465.0, '2021-02-21 18:00:00+00:00'),
                    datetime(2021, 2, 21, 20, 0, 0, 0), 100,
                    Timeframes.FOUR_HOURS.value, 3)

doge_cont_1h = Asset('DOGEBUSD',
                     (0.744998, '2021-05-08 04:00:00+00:00'),
                     (0.6674, '2021-05-08 00:00:00+00:00'),
                     datetime(2021, 5, 8, 5, 0, 0, 0), 100,
                     Timeframes.ONE_HOUR.value, 0)

doge_cont_4h = Asset('DOGEBUSD',
                     (0.744998, '2021-05-08 04:00:00+00:00'),
                     (0.6674, '2021-05-08 00:00:00+00:00'),
                     datetime(2021, 5, 8, 5, 0, 0, 0), 100,
                     Timeframes.ONE_HOUR.value, 0)

btc_rev = Asset('BTCBUSD',
                (58434.0, '2021-02-21 19:00:00+00:00'),
                (57465.0, '2021-02-21 18:00:00+00:00'),
                datetime(2021, 2, 21, 20, 0, 0, 0), 100,
                Timeframes.ONE_HOUR.value, 3)

btc_cont_live_1h = Asset('BTCBUSD',
                         (16880.8, '2022-12-23 10:00:00+00:00'),
                         (16806.6, '2022-12-23 08:00:00+00:00'),
                         datetime(2022, 12, 11, 20, 0, 0, 0), 100,
                         Timeframes.ONE_HOUR.value, 3)
