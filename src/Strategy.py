"""Implement an abstract class as a template for particular strategies.

Classes
----------
Strategy:
    Implements generic properties of strategies that are common amongst all
    particular trading strategies such as buying and selling.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.Assets import Asset, Params, TradeData

import pandas as pd


class Strategy(ABC):
    """Implements generic functions of trades that are common amongst all
    particular trading strategies such as buying and selling.
    """

    def __init__(self):
        pass

    @abstractmethod
    def next_candle_setup(self, asset: Asset,
                          trade_data: TradeData, row: pd.Series) -> None:
        """Checks for valid trade set upss."""

        pass

    @abstractmethod
    def next_candle_trade(self, asset: Asset, params: Params,
                          trade_data: TradeData, row: pd.Series) -> None:
        """Simulate executing trades."""

        pass

    def _long(self, price: float, risk: float, asset: Asset, params: Params,
              trade_data: TradeData) -> None:
        """Enters a long trade.

        Parameters
        ----------
        price : float
            The price at which to buy the asset.
        risk : float
            The risk per trade.
        asset : Asset
            The asset to be traded.
        params : Params
            The parameters for the strategy.
        trade_data : TradeData
            The data log of the current backtest.
        """

        trade_size = min(params.leverage*trade_data.equity,
                         (params.risk/risk) * trade_data.equity)
        coins = round(trade_size/price, asset.decimals)
        trade_data.position += coins
        trade_data.equity -= (1.+trade_data.exchange_fees) * coins*price

    def _short(self, price: float, risk: float, asset: Asset, params: Params,
               trade_data: TradeData) -> None:
        """Enters a short trade.

        Parameters
        ----------
        price : float
            The price at which to sell the asset.
        risk : float
            The risk per trade.
        asset : Asset
            The asset to be traded.
        params : Params
            The parameters for the strategy.
        trade_data : TradeData
            The data log of the current backtest.
        """

        trade_size = min(params.leverage*trade_data.equity,
                         (params.risk/risk) * trade_data.equity)
        coins = round(trade_size/price, asset.decimals)
        trade_data.position -= coins
        trade_data.equity += (1.-trade_data.exchange_fees) * coins*price

    def _close_long_trade(self, price: float, trade_data: TradeData) -> None:
        """Closes an open long or short positoin.

        Parameters
        ----------
        price : float
            The price at which to close the position.
        trade_data : TradeData
            The data log of the current backtest.
        """

        cash = trade_data.position*price
        trade_data.equity += (1.-trade_data.exchange_fees) * cash
        trade_data.position = 0

    def _close_short_trade(self, price: float, trade_data: TradeData) -> None:
        """Closes an open long or short positoin.

        Parameters
        ----------
        price : float
            The price at which to close the position.
        trade_data : TradeData
            The data log of the current backtest.
        """

        cash = trade_data.position*price
        trade_data.equity += (1.-trade_data.exchange_fees) * cash
        trade_data.position = 0


@dataclass
class TradeLog:
    """Encapsulate the four main components of a backtest.

    ...

    Attributes
    ----------
    strategy : Strategy
        The strategy used in the backtest.
    asset : Asset
        The asset traded in the backtest.
    params : Params
        The parameters of the strategy.
    trade_data : TradeData
        The data log of the current backtest.
    """

    strategy: Strategy
    asset: Asset
    params: Params
    trade_data: TradeData


    def simulate(self, data: pd.DataFrame) -> None:
        """Goes through a given set of historical data and applies the trading
        strategy to this data.

        Parameters
        ----------
        data : pd.DataFrame
            The historical data to be simulated.
        """

        for index, row in data.iterrows():
            self.strategy.next_candle_trade(self.asset, self.params,
                                            self.trade_data, row)
            self.strategy.next_candle_setup(self.asset, self.trade_data, row)
