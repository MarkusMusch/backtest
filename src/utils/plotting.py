"""Collect functions for different plotting scenarios."""

import os

import numpy as np
import matplotlib.pyplot as plt

import utils.metrics as metrics
from Strategy import TradeLog


def plot_backtest(trade_log: TradeLog,
                  strategy_name: str,
                  equity_train: np.array,
                  equity_test: np.array) -> None:
    """Plot the equity curve of backtest during ttraining and testing phase
       and a confidence interval of the bootstraped distribution of the
       optimal strategy during training to potentially invalidate the
       equity curve on the testing data.

    Parameters
    ----------
    trade_log : TradeLog
        The trade log of the backtest.
    strategy_name : str
        The name of the strategy.
    equity_train : np.array
        The equity curve of the training phase.
    equity_test : np.array
        The equity curve of the testing phase.
    """

    x_train = len(equity_train)
    x_test = len(equity_test)

    x = np.linspace(0, x_train+x_test-1, x_train+x_test)

    fig, axs = plt.subplots(1, 2, figsize=(15, 8),
                            gridspec_kw={'width_ratios': [5, 1]})

    fig.suptitle('Equity Curve and Performance Metrics of Backtests for '
                 + strategy_name)
    fig.subplots_adjust(hspace=0.4)

    stats_train = metrics.get_stats(equity_train)
    stats_test = metrics.get_stats(equity_test)

    # Bootstrap confidence interval
    sample = np.random.choice(stats_train['returns'],
                              size=(len(stats_test['returns'])+1, 250)) + 1
    sample = np.cumprod(sample, axis=0) * equity_train[-1]
    mean_percentile = np.percentile(sample, 50, axis=1)
    upper_percentile = np.percentile(sample, 95, axis=1)
    lower_percentile = np.percentile(sample, 5, axis=1)

    axs[0].plot(np.concatenate((equity_train, equity_test)), color='b',
                label='Equity Curve')
    axs[0].plot(x[-len(mean_percentile):], mean_percentile, color='y',
                label='Median')
    axs[0].plot(x[-len(upper_percentile):], upper_percentile, color='r',
                label='90% Confidence Interval')
    axs[0].plot(x[-len(lower_percentile):], lower_percentile, color='r')
    axs[0].plot(x[-len(equity_test):], equity_test, color='b',
                label='Equity Curve')

    axs[1].axis('off')
    table = axs[1].table(cellText=[[stats_test['sharpe']],
                                   [stats_test['sortino']],
                                   [stats_test['max_dd']],
                                   [stats_test['musch']]],
                         rowLabels=['Sharpe', 'Sortino',
                                    'Max. Drawdown', 'Musch'],
                         colLabels=['Metrics'], loc='best')
    table.auto_set_column_width(col=[0, 1])

    axs[0].set_ylim([0, 1.1*upper_percentile.max()])
    axs[0].legend()

    axs[0].set_title('Equity Curve ' + trade_log.asset.ticker
                     + ' at max. risk {:.2%} '
                     .format(trade_log.params.risk)
                     + 'with max. leverage {:.1f} '
                     .format(trade_log.params.leverage)
                     + 'and R/R {:.1f} \n'
                     .format(trade_log.params.reward_risk))
    axs[0].grid(True)

    path = './src/backtest_reports/' + strategy_name \
           + '/' + trade_log.asset.ticker + '/'
    if not os.path.exists(path):
        os.makedirs(path)

    plt.savefig(path + trade_log.params.timeframe + '.png', dpi=300)
    print(trade_log.asset.ticker, ' done! \n')
