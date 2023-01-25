from enum import Enum
import os
import sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import numpy as np
import pandas as pd

from Backtest import Backtest
from Assets import btc_cont_1h, Params
from strategies.ContinuationTrade import ContinuationTrade
import utils.metrics as metrics
import utils.plotting as plotting
import utils.telegram as telegram

class Timeframes(Enum):
    ONE_HOUR = '1h'

if __name__ == '__main__':

    bt = Backtest()

    train_test_split = 0.5

    markets = [btc_cont_1h] # , btc_cont_4h, doge_cont_1h, doge_cont_4h]

    risk_samples = np.linspace(0.01, 0.1, 5)
    leverage_samples = [1, 3, 5, 10]
    risk_reward = [2.0, 3.0]
    params_space = []

    for idxr, risk in enumerate(risk_samples):
        for idxl, leverage in enumerate(leverage_samples):
            for idxrr, rr in enumerate(risk_reward):
                params_space.append(Params(risk, rr, leverage))

    df = pd.read_csv('./database/datasets/binance_futures/' +
                     markets[0].market_name + '/' +
                     markets[0].timeframe + '.csv')

    train_idx = round(len(df) * train_test_split)
    df_train = df.iloc[:train_idx]
    df_test = df.iloc[train_idx:]

    optimal_asset, optimal_params, equity_train = bt.train(ContinuationTrade,
                                                           btc_cont_1h,
                                                           params_space,
                                                           df_train,
                                                           metrics.calculate_returns,
                                                           metrics.calculate_sharpe)

    optimal_asset.initial_equity = equity_train[-1]

    equity_test = bt.test(ContinuationTrade, optimal_asset, optimal_params, df_test)

    plotting.plot_backtest(optimal_asset, optimal_params, Timeframes.ONE_HOUR,
                           'Continuation Trade', equity_train, equity_test)

    # telegram.send_message('Backtest Finished!')
