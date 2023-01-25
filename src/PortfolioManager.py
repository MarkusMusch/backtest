"""Implement classes to manage a portfolio of strategies.

Classes
----------
    Portfolio:
        Represents a portfolio of trading strategies.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm

from Strategy import Strategy


class PortfolioManager:
    """Collect several trading strategies into a portfolio of trading
    strategies.

    ...

    Attributes
    ----------
    strategies : list
        List of trading strategies.

    Methods
    -------
    equity_curve() -> float:
        Returns the current equity curve of the portfolio.
    plot_equity() -> None:
        Plot the portfolios equity curve
    add_strategy(strategy: Strategy) -> None:
        Add a new strategy to the portfolio.
    """

    def __init__(self, strategies: list = []):
        """
        Parameters
        ----------
        strategies : list
            List of trading strategies.
        """

        self.strategies = strategies

    @property
    def equity_curve(self) -> float:
        """Returns the current equity curve of the portfolio.

        Returns
        -------
        float
            The current equity curve of the portfolio.
        """

        for idx, strat in enumerate(self.strategies):
            if idx == 0:
                if strat[0].timeframe == '4h':
                    pf = np.repeat(strat[1].equity_curve, 4)
                else:
                    pf = strat[1].equity_curve
            else:
                if strat[0].timeframe == '4h':
                    asset = np.repeat(strat[1].equity_curve, 4)
                else:
                    asset = strat[1].equity_curve

                size_diff = pf.size - asset.size
                if size_diff > 0:
                    asset = np.concatenate((np.full(size_diff, asset[0]),
                                            asset))
                elif size_diff < 0:
                    pf = np.concatenate((np.full(size_diff, pf[0]), pf))
                pf = np.add(pf, asset)

        pf = (1./len(self.strategies))*pf

        return pf

    def plot_equity(self) -> None:
        """Plot the portfolios equity curve."""

        pf = self.equity_curve

        plt.figure(figsize=(18, 9))
        plt.grid(True)
        plt.plot(pf)
        plt.show()

    def add_strategy(self, strategy: Strategy) -> None:
        """Add a new strategy to the portfolio.

        Parameters
        ----------
        strategy : Strategy
            Strategy to add to the portfolio.
        """

        self.strategies.append(strategy)

    def initialize_trades(self) -> None:
        """Go through a given set of historical data and applies the trading
        strategy to this data, tracking results."""

        for idx, strat in enumerate(tqdm(self.strategies)):
            start_time = strat[0].start_time
            
            df = pd.read_csv('./database/datasets/binance_futures/' +
                             strat[0].ticker + '/'
                             + strat[1].timeframe + '.csv')
            df = df[df['open time'] >= int(start_time.timestamp()*1000)]

            for index, row in df.iterrows():
                strat[1].next_candle_trade(row)
                strat[1].next_candle_setup(row)
