from dataclasses import dataclass
import os

import numpy as np
import matplotlib.pyplot as plt

from Assets import Asset
from Stats import Stats

def plot_backtest(market: Asset, params: dataclass, timeframe: str,
                  strategy_name: str,
                  equity_train: np.array,
                  equity_test: np.array) -> None:
    """Plot the backtest."""

    x_train = len(equity_train)
    x_test = len(equity_test)

    x = np.linspace(0, x_train+x_test-1, x_train+x_test)

    stats = Stats()
    fig, axs = plt.subplots(1, 2, figsize=(15, 8),
                            gridspec_kw={'width_ratios': [5, 1]})

    fig.suptitle('Equity Curve and Performance Metrics of Backtests for '
                 + strategy_name)
    fig.subplots_adjust(hspace=0.4)

    # stats.print_stats(rtit.equity_curve)
    stats_train = stats.get_stats(equity_train)
    stats_test = stats.get_stats(equity_test)

    # Bootstrap confidence interval
    sample = np.random.choice(stats_train['returns'],
                              size=(len(stats_test['returns'])+1, 250)) + 1
    sample = np.cumprod(sample, axis=0) * equity_train[-1]
    mean_percentile = np.percentile(sample, 50, axis=1)
    upper_percentile = np.percentile(sample, 95, axis=1)
    lower_percentile = np.percentile(sample, 5, axis=1)

    axs[0].plot(np.concatenate((equity_train, equity_test)), color='k', label='Equity Curve')
    axs[0].plot(x[-len(mean_percentile):], mean_percentile, color='g', label='Median')
    axs[0].plot(x[-len(upper_percentile):], upper_percentile, color='r',
                label='90% Confidence Interval')
    axs[0].plot(x[-len(lower_percentile):], lower_percentile, color='r')
    axs[0].plot(x[-len(equity_test):], equity_test, color='k', label='Equity Curve')

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

    axs[0].set_title('Equity Curve ' + market.market_name 
                     + ' at max. risk {:.2%} '.format(params.risk)
                     + 'with max. leverage {:.1f} '.format(params.leverage)
                     + 'and R/R {:.1f} \n'.format(params.reward_risk))
    axs[0].grid(True)

    path = './src/backtests/backtest_reports/' + strategy_name \
            + '/' + market.market_name + '/'
    if not os.path.exists(path):
        os.makedirs(path)

    plt.savefig(path + timeframe.value + '.pdf', dpi=300)
    print(market.market_name, ' done! \n')