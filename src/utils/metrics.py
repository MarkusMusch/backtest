"""Collect functions to calculate performance metrics from an equity curve."""

import numpy as np

def calculate_returns(equity_curve: np.array) -> np.array:
    """Calculate returns from equity curve.

    Parameters
    ----------
    equity_curve : np.array
        The equity curve of the strategy.

    Returns
    -------
    np.array
        Returns of the strategy.
    """

    returns = np.diff(equity_curve)/equity_curve[:-1]

    return returns

def calculate_max_drawdown(equity_curve: np.array) -> np.array:
    """Calculate the maximum draw down.

    Parameters
    ----------
    equity_curve : np.array
        The equity curve of the strategy.

    Returns
    -------
    np.array
        Maximum draw down of the strategy.
    """

    m_max = 0.
    maxDD = 0.

    for i in range(equity_curve.shape[0]):
        m_max = max(m_max, equity_curve[i])
        maxDD = min(maxDD, equity_curve[i]/m_max - 1)

    return round(maxDD, 3)

def calculate_coeff_of_var(returns: np.array) -> np.array:
    """Calculate the coefficient of variation from the returns.

    Parameters
    ----------
    returns : np.array
        Returns of the strategy.

    Returns
    -------
    np.array
        Coefficient of variation of the strategy.
    """

    mean = returns.mean()
    std = returns.std()

    cov = round(std / mean, 2) if mean != 0 else 0

    return cov

def calculate_sharpe(returns: np.array) -> np.array:
    """Calculate the Sharpe ratio from the returns.

    Parameters
    ----------
    returns : np.array
        Returns of the strategy.

    Returns
    -------
    np.array
        Sharpe ratio of the strategy.
    """

    gap = 1./24
    mean = returns.mean()
    std = returns.std()

    sharpe = round(mean / std * np.sqrt(365/gap), 2) if std != 0 else 0

    return sharpe

def calculate_sortino(returns: np.array) -> np.array:
    """Calculate the Sortino ratio from the returns.

    Parameters
    ----------
    returns : np.array
        Returns of the strategy.

    Returns
    -------
    np.array
        Sortino ratio of the strategy.
    """

    gap = 1./24
    mean = returns.mean()
    downside = (np.square(returns[returns < 0])).sum()
    downside_dev = np.sqrt(downside/returns.size)

    sortino = round(mean / downside_dev * np.sqrt(365/gap), 2) if downside_dev != 0 else 0

    return sortino

def calculate_omega(returns: np.array) -> np.array:
    """Calculate the Omega ratio from the returns.

    Parameters
    ----------
    returns : np.array
        Returns of the strategy.

    Returns
    -------
    np.array
        Omega ratio of the strategy.
    """

    positive_area = returns[returns > 0].sum()
    negative_area = -returns[returns < 0].sum()

    omega = round(positive_area / negative_area, 2) if negative_area != 0 else 0

    return omega

def calculate_musch(equity_curve: np.array) -> np.array:
    """Calculate the Musch ratio from the returns.

    Parameters
    ----------
    returns : np.array
        Returns of the strategy.

    Returns
    -------
    np.array
        Musch ratio of the strategy.
    """

    max_dd = calculate_max_drawdown(equity_curve)
    returns = max(0, (equity_curve[-1] / equity_curve[0])-1)

    musch = 0 if (max_dd == -1 or max_dd == 0) else round(returns / ((1/((1+max_dd)**5)) - 1), 2)

    return musch



def get_stats(equity_curve: np.array) -> dict:
    """Calculate important stats of a strategy and return them in a dict.

    Parameters
    ----------
    equity_curve : np.array
        The equity curve of the strategy.

    Returns
    -------
    dict
        Dictionary containing the stats of the strategy.
    """

    returns = calculate_returns(equity_curve)
    mean = returns.mean()
    std = returns.std()
    max_dd = calculate_max_drawdown(equity_curve)
    coeff_of_var = calculate_coeff_of_var(returns)
    sharpe = calculate_sharpe(returns)
    sortino = calculate_sortino(returns)
    omega = calculate_omega(returns)
    musch = calculate_musch(equity_curve)

    return {'returns': returns, 'mean': mean, 'std': std,
            'max_dd': max_dd, 'coeff_of_var': coeff_of_var,
            'sharpe': sharpe, 'sortino': sortino, 'omega': omega,
            'musch': musch}

def print_stats(equity_curve: np.array) -> None:
    """Calculate and print important stats of the strategy.
    
    Parameters
    ----------
    equity_curve : np.array
        The equity curve of the strategy.
    """

    stats = get_stats(equity_curve)

    print('Mean:            {:.2%}'.format(stats['mean']))
    print('Standard Deviation: {:.2%}'.format(stats['std']))
    print('Max Drawdown:    {:.2%}'.format(stats['max_dd']))
    print('Coefficient of Variation: {:.2f}'.format(stats['coeff_of_var']))
    print('Hourly Sharpe:    {:.2f}'.format(stats['sharpe']))
    print('Hourly Sortino:   {:.2f}'.format(stats['sortino']))
    print('Hourly Omega:     {:.2f} '.format(stats['omega']))
    print('Hourly Musch:     {:.2f} \n'.format(stats['musch']))