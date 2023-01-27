"""Input parameters for the backtest optimization."""

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
from src.Strategy import  TradeLog


class Timeframes(Enum):
    """Timeframes available for backtesting."""

    ONE_HOUR = '1h'
    FOUR_HOURS = '4h'
    ONE_DAY = '1d'

class Strategies(Enum):
    """Strategies available for backtesting."""

    CONTINUATION_TRADE = ContinuationTrade()

# Name of the backtest: will be used as the name of the reports directory
test_name = 'Continuation Trade'
# Fees for the exchange
exchange_fees = 0.0004
# Assets to be backtested
ticker = ('BTCBUSD', 3)
# Strategy to be backtested
strategy = Strategies.CONTINUATION_TRADE.value
# Percentage of the dataset to be used for training
train_test_split = 0.5
# Risk samples to be used for the backtest
risk_samples = np.linspace(0.01, 0.1, 5)
# Leverage samples to be used for the backtest
leverage_samples = [1, 3, 5, 10]
# Risk reward samples to be used for the backtest
risk_reward = [2.0, 3.0]
# Timeframe to be used for the backtest
timeframe = Timeframes.ONE_HOUR.value

if __name__ == '__main__':

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
    
    for idxr, risk in enumerate(risk_samples):
        for idxl, leverage in enumerate(leverage_samples):
            for idxrr, rr in enumerate(risk_reward):
                trade_logs.append(TradeLog(strategy,
                                           asset,
                                           Params(risk, rr, leverage,
                                                  timeframe),
                                           TradeData(exchange_fees)))

    train_idx = round(len(df) * train_test_split)
    df_train = df.iloc[:train_idx]
    df_test = df.iloc[train_idx:]

    optimal_trade = bt.train(trade_logs, df_train,
                             metrics.calculate_returns,
                             metrics.calculate_sharpe)

    equity_train = optimal_trade.trade_data.equity_curve
    optimal_trade.trade_data.equity_curve = \
        np.array([optimal_trade.trade_data.mark_to_market])

    optimal_trade = bt.test(optimal_trade, df_test)
    equity_test = optimal_trade.trade_data.equity_curve

    plotting.plot_backtest(optimal_trade, test_name, equity_train,
                           equity_test)
