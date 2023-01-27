"""Do parameter optimization and testing for a strategy on historical data.

Classes
----------
Backtest:
    Provide parameter optimization and testing for a strategy.
"""

import pandas as pd

from Strategy import TradeLog


class Backtest():
    """Backtests a trading strategy on historical data."""

    def __init__(self):
        pass

    def _simulate(self, log: TradeLog, data: pd.DataFrame) -> None:
        """Goes through a given set of historical data and applies the trading
        strategy to this data.
        
        Parameters
        ----------
        log : TradeLog
            The data log of the current backtest.
        data : pd.DataFrame
            The historical data to be simulated.
        """

        for index, row in data.iterrows():
            log.strategy.next_candle_trade(log.asset, log.params,
                                           log.trade_data, row)
            log.strategy.next_candle_setup(log.asset, log.trade_data, row)

    def train(self, trade_logs: list, data: pd.DataFrame,
              return_metric: callable, reward_metric: callable) -> TradeLog:
        """Train the model on a set of training data.
        
        Parameters
        ----------
        trade_logs : list
            A list of candidates for optimal strategy.
        data : pd.DataFrame
            The historical data to be simulated.
        return_metric : callable
            The function to compute the returns of a trade.
        reward_metric : callable
            The metric to be used to evaluate the performance of a trade.

        Returns
        -------
        TradeLog
            The strategy that performed best on training data.
        """

        log = trade_logs.pop(0)
        self._simulate(log, data)

        returns = return_metric(log.trade_data.equity_curve)
        reward_tmp = reward_metric(returns)

        optimal_trade = log
        reward_max = reward_tmp

        for log in trade_logs:

            self._simulate(log, data)

            returns = return_metric(log.trade_data.equity_curve)
            reward_tmp = reward_metric(returns)

            if reward_tmp > reward_max:
                optimal_trade = log
                reward_max = reward_tmp

        return optimal_trade

    def test(self, optimal_trade: TradeLog, data: pd.DataFrame) -> None:
        """Test the trained model on prviously unknown test data.
        
        Parameters
        ----------
        optimal_trade : TradeLog
            The strategy that performed best on training data.
        data : pd.DataFrame
            The historical data to be simulated.
        """

        self._simulate(optimal_trade, data)

        return optimal_trade
