from enum import Enum
import os
import sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from Backtest import Backtest
from Assets import btc_cont_1h
from strategies.ContinuationTrade import ContinuationTrade
from Stats import Stats

class Timeframes(Enum):
    ONE_HOUR = '1h'

if __name__ == '__main__':

    stats = Stats()
    bt = Backtest()

    markets = [btc_cont_1h] # , btc_cont_4h, doge_cont_1h, doge_cont_4h]

    risk_samples = [0.05] # , 0.02, 0.01, 0.075, 0.1]
    leverage_samples = [1] # , 3, 5, 10]
    risk_reward = [2.0, 3.0]

    for market in markets:
        bt.run(ContinuationTrade, market, risk_samples, leverage_samples,
               risk_reward, Timeframes)

    bt.send_message('Backtest Finished!')
