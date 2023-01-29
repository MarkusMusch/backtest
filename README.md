# Backtest

This is a spin-off of the [bot](https://github.com/MarkusMusch/bot) repository focusing solely on the backtesting engine.

## Includes:

1. **Building your own backtests**

	* A ready-to-use backtest for an example strategy, making it easy to get started with backtesting your own strategies.

2. **Training your model**

	* The Backtest class provides a train and a test method making it easy to do parameter optimizations and test the results for validity. This way, you can plug in your own strategies and see how they would have fared under different market conditions in the past.

3. **Testing your model**

	* Backtest reports for the example strategy that provide a comprehensive overview of the strategy's performance, including plots of the equity curve, confidence intervals of bootstraped returns, and important performance metrics for different parameters.

	<p align="center">
	<img src="https://github.com/MarkusMusch/backtest/blob/main/images/BTCBUSD_1h.png" />
	</p>

    > The backtest in the image above shows the return curve optimized for maximal Sharpe ratio on the first 75% of the data and the equity curve of the same strategy on the test data together with the median and 90% confidence interval of 250 samples bootstraped from the returns of the strategy that performed best on the training data. On the right hand side, a table with performance metrics for the equity curve on the test data is being shown.

## Installation

First, clone the repository.

 ```bash
 git clone 'https://github.com/MarkusMusch/backtest.git' && cd backtest/
 ```
 
 Second, install all third party libraries necessary. Those are all listed in the [requirements.txt](requirements.txt).

 ```bash
 pip install -r requirements.txt
 ```

## Usage

### Writing a Strategy

We utilize the *Strategy Design Pattern* to provide a unified interface for applying different trading strategies in backtests. The actual logic of each individual trading strategy is implemented in a derived class of the interface and therefore easily interchangeable. For this purpose, we implement an abstract class called *Strategy*, that only implements the methods that all strategies have in common, namely ```_long```, ```_short```, ```_close_long_trade``` and ```_close_short_trade```. At the same time, it also provides two abstract methods ```next_candle_setup``` and ```next_candle_trade``` that provide the interface for users of this class, which have to be implemented by each derived class.

Our example is a strategy that bets on the continuation of an ongoing trend. If the market is in an up-trend, and certain criteria are met, the strategy enters a long trade to profit from the continuation of the up-trend. In the same way, we enter a short trade if the market is in an ongoing down-trend.

Whilst the abstract strategy class is in the *backtest/src* directory, the actual implementation of a particular strategy is in the *backtest/src/strategies* directory. 

So, to implement our trend continuation strategy, we create a new file in the *backtest/src/strategies* directory. In our case it is called *ContinuationTrade.py*. In this file we implement the trade logic in a class that inherits from *Strategy*.

<p align="center">
  <img src="https://github.com/MarkusMusch/backtest/blob/main/images/Strategy_UML.png"
  width=50%>
</p>

The *Strategy* base class has two abstract methods that we have to implement in our child class.

The ```next_candle_setup``` and ```next_candle_trade``` methods give a public interface for our backtest modules.

The ```next_candle_trade``` method checks if a new trigger has been set or if there is an existing position and calls the ```_long```, ```_short```, ```_exit_long_trade```, or ```_exit_short_trade``` method respectively.

If ```_long``` or ```_short``` is being called some more conditions such as a sufficient reward/risk ratio are being checked. If those conditions are satisfied a trade is being recorded in a trade log for backtesting.

If ```_exit_long_trade``` or ```_exit_short_trade``` is being called the current trade is being noted as closed on the trade for backtesting.

<p align="center">
<img src="https://github.com/MarkusMusch/backtest/blob/main/images/strategy_control_flow.png" />
</p>

This diagram shows the whole control flow described above.

### Writing Backtests

#### Writing Single Strategy Backtests

To encapsulate the tradable tickers, timeframes, and strategies we collect each of those in an ```Enum```, respectively.

If you want to trade markets that are not included in the current code, make sure to define them in the *Tickers* Enum and download the necessary price data.

Currently, there is support for perpetual futures on the 9 different BUSD pairs you can see bellow.

```Python
class Tickers(Enum):
    """Tickers available for backtesting."""

    BTCBUSD = ('BTCBUSD', 3)
    ETHBUSD = ('ETHBUSD', 3)
    SOLBUSD = ('SOLBUSD', 0)
    BNBBUSD = ('BNBBUSD', 2)
    DOGEBUSD = ('DOGEBUSD', 0)
    LINKBUSD = ('LINKBUSD', 1)
    LTCBUSD = ('LTCBUSD', 2)
    MATICBUSD = ('MATICBUSD', 0)
    XRPBUSD = ('XRPBUSD', 1)
```

For those trading pairs, price data on the following time frames is available:

```Python
class Timeframes(Enum):
    """Timeframes available for backtesting."""

    FIVE_MINUTES = '5m'
    FIFTEEN_MINUTES = '15m'
    THIRTY_MINUTES = '30m'
    ONE_HOUR = '1h'
    FOUR_HOURS = '4h'
    ONE_DAY = '1d'
```

After importing your own strategies, you add them to the *Strategies* Enum which currently only contains the included *Continuation Trade* strategy.

```Python
class Strategies(Enum):
    """Strategies available for backtesting."""

    CONTINUATION_TRADE = (ContinuationTrade(), 'Continuation Trade')
```

To set up a new backtest for an individual strategy, the only thing you have to do is set the desired parameters in the *backtest.py* module.

You can change the preset ticker and strategy, and adjust the set of risk levels, leverage sizes, and reward/risk ratios if the predefined ones do not fit your particular use case.

```Python
# Fees for the exchange
exchange_fees = 0.0004
# Assets to be backtested
ticker = Tickers.BTCBUSD.value
# Strategy to be backtested
strategy, test_name = Strategies.CONTINUATION_TRADE.value
# Percentage of the dataset to be used for training
train_test_split = 0.75
# Risk samples to be used for the backtest
risk_samples = np.linspace(0.01, 0.1, 5)
# Leverage samples to be used for the backtest
leverage_samples = [1, 3, 5, 10]
# Risk reward samples to be used for the backtest
risk_reward = [2.0, 3.0]
# Timeframe to be used for the backtest
timeframe = Timeframes.ONE_HOUR.value
```

A report of your backtest will be saved in the *backtest/src/backtest_reports* directory including equity curves and important performance metrics such as Sharpe Ratio, Sortino Ratio, and Maximum Draw Down of your test run.

### Unit Tests

To run the included unit tests execute

```bash
pytest-3 -v
```

## Contributing

1. Fork it (https://github.com/MarkusMusch/backtest/fork)
2. Create your feature branch (git checkout -b feature/fooBar)
3. Commit your changes (git commit -am 'Add some fooBar')
4. Push to the branch (git push origin feature/fooBar')
5. Create a new Pull Request

If you are serious about  contributing to the project or you have a similar project and are keen to discuss coding or trading, reach out to me.

## License and author info

### Author

Markus Musch

### License

See the [LICENSE](LICENSE.txt) file for license rights and limitations (GNU GPLv3).
