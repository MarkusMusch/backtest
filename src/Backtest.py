import copy
from datetime import datetime, timedelta
import pandas as pd

from Assets import Asset, Params
from MarketStructure import MarketStructure
from Strategy import Strategy


class Backtest():
    """Backtests a trading strategy on historical data."""

    def __init__(self):
        pass

    def _simulate(self, strat: Strategy, data: pd.DataFrame) -> None:
        """Goes through a given set of historical data and applies the trading
        strategy to this data."""

        for index, row in data.iterrows():
            strat.next_candle_trade(row)
            strat.next_candle_setup(row)

    def train(self, trade: Strategy, market: Asset, params_space: list,
              data: pd.DataFrame, return_metric: callable, reward_metric: callable) -> Asset:
        """Train the model."""

        ath = market.ath
        prev_low = market.prev_low
        reward_max = 0
        asset_opt = copy.deepcopy(market)

        for params in params_space:

            ms = MarketStructure(ath, prev_low, ath, prev_low)
            rtit = trade(ms, market, params)

            self._simulate(rtit, data)

            returns = return_metric(rtit.equity_curve)
            reward_tmp = reward_metric(returns)

            if reward_tmp > reward_max:
                optimal_params = params
                asset_opt = copy.deepcopy(market)
                equity = rtit.equity_curve
                reward_max = reward_tmp

        return asset_opt, optimal_params, equity

    def test(self, trade: Strategy, market: Asset, params: Params,
             data: pd.DataFrame) -> None:
        """Test the trained model."""

        ms = MarketStructure(market.ath, market.prev_low, market.ath,
                             market.prev_low)
        rtit = trade(ms, market, params)

        self._simulate(rtit, data)

        return rtit.equity_curve
        

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