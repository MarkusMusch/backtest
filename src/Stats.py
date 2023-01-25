"""Implement a class to calculate stats for strategies and portfolios.

Classes
----------
    Stats:
        Implements methods to calculate stats for strategies and
        portfolios given the equity curve of a strategy or protfolio.
"""

import numpy as np

import utils.metrics as metrics

class Stats:
    """Calculate statistics and make plots of strategies and portfolios equity
    curves.

    ...

    Methods
    -------
    get_stats(equity_curve: np.array) -> dict:
        Calculate important stats and return them in a dict.
    """

    def __init__(self):
        pass

    def get_stats(self, equity_curve: np.array) -> dict:
        """Calculate important stats of a strategy and return them in a dict.

        Parameters
        ----------
        equity_curve : np.array
            The equity curve of the strategy.
        """

        returns = metrics.calculate_returns(equity_curve)
        mean = returns.mean()
        std = returns.std()
        max_dd = metrics.calculate_max_drawdown(equity_curve)
        coeff_of_var = metrics.calculate_coeff_of_var(returns)
        sharpe = metrics.calculate_sharpe(returns)
        sortino = metrics.calculate_sortino(returns)
        omega = metrics.calculate_omega(returns)
        musch = metrics.calculate_musch(equity_curve)

        return {'returns': returns, 'mean': mean, 'std': std,
                'max_dd': max_dd, 'coeff_of_var': coeff_of_var,
                'sharpe': sharpe, 'sortino': sortino, 'omega': omega,
                'musch': musch}

    def print_stats(self, equity_curve: np.array) -> None:
        """Calculate and print important stats of the strategy."""

        stats = self.get_stats(equity_curve)

        print('Mean:            {:.2%}'.format(stats['mean']))
        print('Standard Deviation: {:.2%}'.format(stats['std']))
        print('Max Drawdown:    {:.2%}'.format(stats['max_dd']))
        print('Coefficient of Variation: {:.2f}'.format(stats['coeff_of_var']))
        print('Hourly Sharpe:    {:.2f}'.format(stats['sharpe']))
        print('Hourly Sortino:   {:.2f}'.format(stats['sortino']))
        print('Hourly Omega:     {:.2f} '.format(stats['omega']))
        print('Hourly Musch:     {:.2f} \n'.format(stats['musch']))
