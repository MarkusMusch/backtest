from enum import Enum
import os
import sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import numpy as np
import pandas as pd

from src.Assets import Asset, Params, TradeData
from src.Backtest import Backtest
from src.strategies.ContinuationTrade import ContinuationTrade
from src.MarketStructure import MarketStructure
import src.utils.metrics as metrics
import src.utils.plotting as plotting
from src.strategies.ReversalTrade import ReversalTrade
from src.Strategy import  TradeLog
import src.utils.telegram as telegram


class Timeframes(Enum):
    ONE_HOUR = '1h'
    FOUR_HOURS = '4h'
    ONE_DAY = '1d'


class Strategies(Enum):
    CONTINUATION_TRADE = ContinuationTrade()
    REVERSAL_TRADE = ReversalTrade()


test_name = 'Continuation Trade'
strategy = Strategies.CONTINUATION_TRADE.value
exchange_fees = 0.0004
# tickers = [{"symbol": "BTCBUSD", "decimals": 3}] # ass.coins

# eth = Asset('ETHBUSD', 3)

# sol = Asset('SOLBUSD', 0)

# bnb = Asset('BNBBUSD', 2)

# doge = Asset('DOGEBUSD', 0)

# coins = [btc, eth, sol, bnb, doge]
tickers = [('BTCBUSD', 3)]
train_test_split = 0.5
risk_samples = np.linspace(0.01, 0.1, 10)
leverage_samples = np.linspace(1, 5, 5)
risk_reward = np.linspace(1, 4, 7)
timeframe = Timeframes.ONE_HOUR.value

if __name__ == '__main__':

    for ticker in tickers:
        bt = Backtest()
        trade_logs = []

        df = pd.read_csv('./database/datasets/binance_futures/' +
                        ticker[0] + '/' +
                        timeframe + '.csv')

        first_price = df.iloc[0]
        date = first_price['open time']
        ms = MarketStructure((first_price.high, date),
                             (first_price.low, date),
                             (first_price.high, date),
                             (first_price.low, date))
        asset = Asset(ticker[0], ticker[1], ms)

        train_idx = round(len(df) * train_test_split)
        df_train = df.iloc[:train_idx]
        df_test = df.iloc[train_idx:]
        for idxr, risk in enumerate(risk_samples):
            for idxl, leverage in enumerate(leverage_samples):
                for idxrr, rr in enumerate(risk_reward):
                    trade_logs.append(TradeLog(strategy,
                                               asset,
                                               Params(risk, rr, leverage,
                                                      timeframe),
                                               TradeData(exchange_fees)))

        optimal_trade = bt.train(trade_logs, df_train,
                                 metrics.calculate_returns,
                                 metrics.calculate_sharpe)

        equity_train = optimal_trade.trade_data.equity_curve
        optimal_trade.trade_data.equity_curve = \
            np.array([optimal_trade.trade_data.equity])

        optimal_trade = bt.test(optimal_trade, df_test)
        equity_test = optimal_trade.trade_data.equity_curve

        plotting.plot_backtest(optimal_trade, test_name, equity_train,
                               equity_test)

        telegram.send_message('Backtest Finished!')
