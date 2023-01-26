from datetime import datetime, timedelta
import pandas as pd

from Strategy import Strategy, TradeLog


class Backtest():
    """Backtests a trading strategy on historical data."""

    def __init__(self):
        pass

    def _simulate(self, log: TradeLog, data: pd.DataFrame) -> None:
        """Goes through a given set of historical data and applies the trading
        strategy to this data."""

        for index, row in data.iterrows():
            log.strategy.next_candle_trade(log.asset, log.params,
                                           log.trade_data, row)
            log.strategy.next_candle_setup(log.asset, log.trade_data, row)

    def train(self, trade_logs: list, data: pd.DataFrame,
              return_metric: callable, reward_metric: callable) -> TradeLog:
        """Train the model."""

        reward_max = 0
        optimal_trade = None

        for log in trade_logs:

            self._simulate(log, data)

            returns = return_metric(log.trade_data.equity_curve)
            reward_tmp = reward_metric(returns)

            if reward_tmp > reward_max:
                optimal_trade = log
                reward_max = reward_tmp

        return optimal_trade

    def test(self, optimal_trade: TradeLog, data: pd.DataFrame) -> None:
        """Test the trained model."""

        self._simulate(optimal_trade, data)

        return optimal_trade
        

class BacktestTwoTF(Backtest):

    def __init__(self):
        pass

    def backtest(self, strat: Strategy, timeframe: str,
                 market_name: str, start: datetime):
        """Goes through a given set of historical data and applies the trading
        strategy to this data."""

        df = pd.read_csv('./database/datasets/binance_futures/' +
                         market_name + '/' + timeframe + '.csv')
        df = df[df['open time'] >= int(start.timestamp()*1000)]

        df_ltf = pd.read_csv('./database/datasets/binance_futures/' +
                                market_name + '/5m.csv')
        df_ltf = df_ltf[df_ltf['open time'] >= int(start.timestamp()*1000)]

        for index, row in df.iterrows():
            strat.next_candle_trade(row)

            start_time = row['open time']
            end_time = start_time + timedelta(minutes=60).microseconds
            tmp = df_ltf[df_ltf['open time'] <= end_time]
            tmp = tmp[tmp['open time'] >= start_time]
            for index, row_ltf in tmp.iterrows():
                strat.next_candle_trade_low_tf(row_ltf)

            strat.next_candle_setup(row)