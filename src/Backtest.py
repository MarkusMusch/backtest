import configparser
from datetime import datetime, timedelta
import os
from enum import Enum

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests

from Assets import Asset
from MarketStructure import MarketStructure
from Stats import Stats
from Strategy import Strategy


class Backtest():
    """Backtests a trading strategy on historical data."""

    def __init__(self):
        pass


    def send_message(self, message: str):
        """Sends a message to a Telegram group."""

        config = configparser.ConfigParser()
        config.read(os.path.expanduser('~') + '/config.ini')

        bot_token = config['Telegram Dev']['bot_token']
        group_id = config['Telegram Dev']['group_id']

        params = {'chat_id': group_id, 'text': message, 'parse_mode': 'HTML'}
        response = requests.post('https://api.telegram.org/bot{}/sendMessage'
                                .format(bot_token), params)

    def backtest(self, strat: Strategy, timeframe: str, market_name: str,
                 start: datetime):
        """Goes through a given set of historical data and applies the trading
        strategy to this data."""

        df = pd.read_csv('./database/datasets/binance_futures/' +
                         market_name + '/' + timeframe + '.csv')
       # df = df[df['open time'] >= int(start.timestamp()*1000)]

        for index, row in df.iterrows():
            strat.next_candle_trade(row)
            strat.next_candle_setup(row)

    def run(self, trade: Strategy, market: Asset,
            risk_samples: list, leverage_samples: list,
            risk_reward: list, timeframes: Enum) -> None:
        """Runs the backtest for a given set of markets."""

        stats = Stats()
        num_rr_ratios = len(risk_reward)
        num_risk_samples = len(risk_samples)
        num_lev_samples = len(leverage_samples)
        market_name = market.market_name
        ath = market.ath
        prev_low = market.prev_low
        start = market.start_time

        for timeframe in timeframes:

            fig, axs = plt.subplots(num_risk_samples*num_lev_samples
                                    * num_rr_ratios, 2, 
                                    figsize=(15, 5 * num_risk_samples
                                             * num_lev_samples
                                             * num_rr_ratios),
                                    gridspec_kw={'width_ratios': [5, 1]})
            fig.suptitle('Equity Curves and Position Sizes of Backtests for '
                         + market.strategy_name)
            fig.subplots_adjust(hspace=0.4)

            for idxr, risk in enumerate(risk_samples):

                for idxl, leverage in enumerate(leverage_samples):

                    for idxrr, rr in enumerate(risk_reward):

                        market.timeframe = timeframe.value
                        market.max_risk = risk
                        market.max_leverage = leverage
                        market.risk_reward = rr

                        ms = MarketStructure(ath, prev_low, ath, prev_low)
                        rtit = trade(ms, market)

                        self.backtest(rtit, timeframe.value, market_name,
                                      start)

                        # stats.print_stats(rtit.equity_curve)
                        stats_dict = stats.get_stats(rtit.equity_curve)

                        idx_subplot = + num_lev_samples*num_rr_ratios*idxr \
                            + num_rr_ratios*idxl + idxrr

                        sample = np.random.choice(stats_dict['returns'],
                                                  size=(len(stats_dict['returns']), 250)) + 1
                        sample = np.cumprod(sample, axis=0) * 100
                        mean_percentile = np.percentile(sample, 50, axis=1)
                        upper_percentile = np.percentile(sample, 95, axis=1)
                        lower_percentile = np.percentile(sample, 5, axis=1)
                        axs[idx_subplot][0].plot(sample, color='y', alpha=0.05)
                        axs[idx_subplot][0].plot(mean_percentile, color='g',
                                                 label='50% Confidence Interval')
                        axs[idx_subplot][0].plot(upper_percentile, color='r',
                                                 label='90% Confidence Interval')
                        axs[idx_subplot][0].plot(lower_percentile, color='r')
                        axs[idx_subplot][0].plot(rtit.equity_curve, color='k',
                                                 label='Equity Curve')

                        axs[idx_subplot][1].axis('off')
                        table = axs[idx_subplot][1].table(cellText=[[stats_dict['sharpe']],
                                                         [stats_dict['sortino']],
                                                         [stats_dict['max_dd']],
                                                         [stats_dict['musch']]],
                                               rowLabels=['Sharpe', 'Sortino',
                                                          'Max. Drawdown',
                                                          'Musch'],
                                               colLabels=['Metrics'], loc='best')
                        table.auto_set_column_width(col=[0, 1])

                        axs[idx_subplot][0].set_ylim([0, 1.1*upper_percentile.max()])
                        axs[idx_subplot][0].legend()

                        axs[idx_subplot][0].set_title(
                            'Equity Curve ' + market_name
                            + ' at max. risk {:.2%} '.format(risk)
                            + 'with max. leverage {:.1f} '.format(leverage)
                            + 'and R/R {:.1f} \n'.format(rr))
                        axs[idx_subplot][0].grid(True)

            path = './src/backtests/backtest_reports/' + market.strategy_name \
                   + '/' + market_name + '/'
            if not os.path.exists(path):
                os.makedirs(path)

            plt.savefig(path + timeframe.value + '.pdf', dpi=300)
        print(market_name, ' done! \n')
        ms.structure


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