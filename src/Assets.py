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
    max_risk : float
        The maximum risk per trade.
    max_leverage : float
        The maximum leverage to be used.
    risk_reward : float
        The risk reward ratio to be used.
    decimals : int
        The maximum number of decimals allowed for the asset.
    """

    strategy: Strategy
    strategy_name: str
    market_name: str
    ath: tuple
    prev_low: tuple
    start_time: datetime
    initial_equity: float
    timeframe: str
    max_risk: float
    max_leverage: float
    risk_reward: float
    decimals: int


btc_cont_1h_5m = Asset(TwoTFContinuationTrade, 'Two_TF_Continuation_Trade',
                       'BTCBUSD', (58434.0, '2021-02-21 19:00:00+00:00'),
                       (57465.0, '2021-02-21 18:00:00+00:00'),
                       datetime(2021, 2, 21, 20, 0, 0, 0), 100,
                       Timeframes.ONE_HOUR.value, 0.1, 1.0, 2.0, 3)

eth_cont_1h_5m = Asset(TwoTFContinuationTrade, 'Two_TF_Continuation_Trade',
                       'ETHBUSD', (4875.4, '2021-11-10 14:00:00+00:00'),
                       (4697.8, '2021-11-10 12:00:00+00:00'),
                       datetime(2021, 11, 10, 15, 0, 0, 0), 100,
                       Timeframes.ONE_HOUR.value, 0.05, 1.0, 3.0, 3)

sol_cont_1h_5m = Asset(TwoTFContinuationTrade, 'Two_TF_Continuation_Trade',
                       'SOLBUSD', (261.5175, '2021-11-06 21:00:00+00:00'),
                       (252.49, '2021-11-06 20:00:00+00:00'),
                       datetime(2021, 11, 6, 22, 0, 0, 0), 100,
                       Timeframes.ONE_HOUR.value, 0.01, 1.0, 3.0, 0)

bnb_cont_1h_5m = Asset(TwoTFContinuationTrade, 'Two_TF_Continuation_Trade',
                       'BNBBUSD', (693.775, '2021-05-10 06:00:00+00:00'),
                       (671.355, '2021-05-10 05:00:00+00:00'),
                       datetime(2021, 5, 10, 7, 0, 0, 0), 100,
                       Timeframes.ONE_HOUR.value, 0.01, 5.0, 3.0, 2)

doge_cont_1h_5m = Asset(TwoTFContinuationTrade, 'Two_TF_Continuation_Trade',
                        'DOGEBUSD', (0.744998, '2021-05-08 04:00:00+00:00'),
                        (0.6674, '2021-05-08 00:00:00+00:00'),
                        datetime(2021, 5, 8, 5, 0, 0, 0), 100,
                        Timeframes.ONE_HOUR.value, 0.01, 3.0, 3.0, 0)

btc_cont_1h = Asset(ContinuationTrade, 'Continuation_Trade', 'BTCBUSD',
                    (58434.0, '2021-02-21 19:00:00+00:00'),
                    (57465.0, '2021-02-21 18:00:00+00:00'),
                    datetime(2021, 2, 21, 20, 0, 0, 0), 100,
                    Timeframes.ONE_HOUR.value, 0.1, 1.0, 2.0, 3)

btc_cont_4h = Asset(ContinuationTrade, 'Continuation_Trade', 'BTCBUSD',
                    (58434.0, '2021-02-21 19:00:00+00:00'),
                    (57465.0, '2021-02-21 18:00:00+00:00'),
                    datetime(2021, 2, 21, 20, 0, 0, 0), 100,
                    Timeframes.FOUR_HOURS.value, 0.1, 1.0, 2.0, 3)

doge_cont_1h = Asset(ContinuationTrade, 'Continuation_Trade', 'DOGEBUSD',
                  (0.744998, '2021-05-08 04:00:00+00:00'),
                  (0.6674, '2021-05-08 00:00:00+00:00'),
                  datetime(2021, 5, 8, 5, 0, 0, 0), 100,
                  Timeframes.ONE_HOUR.value, 0.01, 3.0, 3.0, 0)

doge_cont_4h = Asset(ContinuationTrade, 'Continuation_Trade', 'DOGEBUSD',
                  (0.744998, '2021-05-08 04:00:00+00:00'),
                  (0.6674, '2021-05-08 00:00:00+00:00'),
                  datetime(2021, 5, 8, 5, 0, 0, 0), 100,
                  Timeframes.ONE_HOUR.value, 0.01, 10.0, 2.0, 0)

btc_rev = Asset(ReversalTrade, 'Reversal_Trade', 'BTCBUSD',
                (58434.0, '2021-02-21 19:00:00+00:00'),
                (57465.0, '2021-02-21 18:00:00+00:00'),
                datetime(2021, 2, 21, 20, 0, 0, 0), 100,
                Timeframes.ONE_HOUR.value, 0.01, 1.0, 2.0, 3)

btc_cont_live_1h = Asset(ContinuationTrade, 'Continuation_Trade', 'BTCBUSD',
                         (16880.8, '2022-12-23 10:00:00+00:00'),
                         (16806.6, '2022-12-23 08:00:00+00:00'),
                         datetime(2022, 12, 11, 20, 0, 0, 0), 100,
                         Timeframes.ONE_HOUR.value, 0.1, 1.0, 2.0, 3)

btc_cont_live_4h = Asset(ContinuationTrade, 'Continuation_Trade', 'BTCBUSD',
                         (16880.8, '2022-12-23 10:00:00+00:00'),
                         (16806.6, '2022-12-23 08:00:00+00:00'),
                         datetime(2022, 12, 11, 20, 0, 0, 0), 100,
                         Timeframes.FOUR_HOURS.value, 0.1, 1.0, 2.0, 3)

doge_cont_live_1h = Asset(ContinuationTrade, 'Continuation_Trade', 'DOGEBUSD',
                          (0.07899, '2022-12-23 05:00:00+00:00'),
                          (0.07676, '2022-12-22 23:00:00+00:00'),
                          datetime(2022, 12, 23, 6, 0, 0, 0), 100,
                          Timeframes.ONE_HOUR.value, 0.01, 3.0, 3.0, 0)

doge_cont_live_4h = Asset(ContinuationTrade, 'Continuation_Trade', 'DOGEBUSD',
                          (0.07899, '2022-12-23 05:00:00+00:00'),
                          (0.07676, '2022-12-22 23:00:00+00:00'),
                          datetime(2022, 12, 23, 6, 0, 0, 0), 100,
                          Timeframes.ONE_HOUR.value, 0.01, 10.0, 2.0, 0)

btc_rev_live = Asset(ReversalTrade, 'Reversal_Trade', 'BTCBUSD',
                     (16880.8, '2022-12-23 10:00:00+00:00'),
                     (16806.6, '2022-12-23 08:00:00+00:00'),
                     datetime(2022, 12, 11, 20, 0, 0, 0), 100,
                     Timeframes.ONE_HOUR.value, 0.01, 1.0, 2.0, 3)
