# Backtest

This is a spin off of the [bot](https://github.com/MarkusMusch/bot) repository focusing solely on the backtesting engine.

## Includes:

1. **Building**

	* Two ready-to-use examples for an example strategy and an example portfolio, making it easy to get started with backtesting your own strategies.

2. **Training your model**

	* The Backtest class serves as a template for backtesting, making it easy to plug in your own strategies and see how they would have fared under different market conditions in the past.

3. **Testing your model**

	* Backtest reports for the example strategy that provide a comprehensive overview of the strategy's performance, including plots of the equity curve and important performance metrics for different parameters.

	<p align="center">
	<img src="https://github.com/MarkusMusch/backtest/blob/main/images/BTCBUSD_1h.png" />
	</p>

    > The backtest in the image above shows the return curve optimized for maximal Sharpe ratio on the first 75% of the data and the equity curve of the same strategy on the test data together with the median and 90% confidence interval of 250 samples bootstraped from the returns of the optimal strategy in the training data.

## Installation

First, clone the repository.

 ```bash
 git clone 'https://github.com/MarkusMusch/backtest.git' && cd bot/
 ```
 
 Second, install all third party libraries necessary. Those are all listed in the [requirements.txt](requirements.txt).

 ```bash
 pip install -r requirements.txt
 ```

## Usage

### Writing a Strategy

Our example is a strategy that bets on the continuation of an ongoing trend. If the market is in an up-trend, and certain criteria are met, the strategy enters a long trade to profit from the continuation of the up-trend. In the same way, we enter a short trade if the market is in an ongoing down-trend.

Whilst the abstract strategy class is in the bot/src/ directory, the actual implementation of a particular strategy is in the bot/src/strategies directory. 

So, to implement our trend continuation strategy, we create a new file in the bot/src/strategies/ directory. In our case it is called ContinuationTrade.py. In this file we implement the trade logic in a class that inherits from Strategy.

<p align="center">
  <img src="https://github.com/MarkusMusch/bot/blob/main/images/strategy_inheritance.png"
  width=50%>
</p>

The Strategy base class has a total of eight abstract methods that we have to implement in our child class.

The ```next_candle_init``` and ```next_candle_live``` methods give a public interface for our backtest and live trading modules to distinguish between initialization, backtesting, and live trading.

If we are initializing a strategy for live trading, we call the ```next_candle_init``` method. 


```Python
def  next_candle_init(self, row: pd.Series) -> None:
	"""Initializes the strategy by iterating through historical data
	without executing trades.

	Parameters
	----------
	row : pd.Series
	Row of historical data.
	"""

	self._setup_trade(row)
```


This method calls the ```setup_trade``` methods.

The ```setup_trade``` method checks if a trade set up has been triggered with the recent candle, and if yes, sets the trigger flag for a long or a short set up to ```True```.

If we are not trading live, we record the current equity in every step to evaluate the equity curve later on.

If we are trading live or running a backtest, we call the ```next_candle_live``` method.



```Python
def  next_candle_live(self, row: pd.Series) -> None:
"""Checks for valid trade set ups with new live data and execute live
trades.

Parameters
----------
row : pd.Series
Row of live data.
"""

self._execute_trade(row)
self._setup_trade(row)
```


This method calls both the ```execute_trade``` method to generate trading signals, and the ```setup_trade``` method to detect new set ups.

The ```execute_trade``` method checks if a new trigger has been set or if there is an existing position and calls the ```entry_long```, ```entry_short```, ```exit_long```, or ```exit_short``` method respectively.

If ```entry_long``` or ```entry_short``` is being called some more conditions such as a sufficient reward/risk ratio are being checked. If those conditions are satisfied a trade is being entered on exchange via our RESTClient object for live trading, or recorded without actual execution for backtesting.

If ```exit_long``` or ```exit_short``` is being called the current trade is being closed on exchange via our RESTClient object for live trading, or recorded without actual execution for backtesting.


<p align="center">
<img src="https://github.com/MarkusMusch/bot/blob/main/images/strategy_control_flow.png" />
</p>

This diagram shows the whole control flow described above.

### Writing Backtests: Single Strategies and Full Portfolios

#### Single Strategy Backtest
To set up a new backtest for an individual strategy, you will create a new .py file in the bot/back_tests/ directory with the name of your backtest.

You can copy paste the code from the exisiting backtest_continuation_trade.py module. In this module, we backtest the continuation trade strategy. For this we import the ContinuationTrade class like this:

```Python
from  src.strategies.ContinuationTrade  import  ContinuationTrade
```

You will replace this import line with the module and class of your own strategy. You can also change the preset list of markets and adjust the set of risk levels, leverage sizes, and reward/risk ratios if the predefined ones do not fit your particular use case.

```Python  
markets = [btc_cont, eth_cont, sol_cont, doge_cont]

risk_samples = [0.001, 0.005 , 0.01, 0.05, 0.1, 0.2]
leverage_samples = [1 , 3, 5, 10]
risk_reward = [2.0, 3.0]
```
If you want to trade markets that are not included in the current code, make sure to define them in the Assets.py module and import them.

The last step is to loop through all markets and run the backtests. Here you have to change the second argument "ContinuationTrade" to be *your* strategy.

```Python
for  market  in  markets:
	bt.run(ec, ContinuationTrade, market, risk_samples, leverage_samples,
		   risk_reward, Timeframes)
```
The Backtest object will also save a report of you backtest in the bot/back_tests/backtest_reports/ directory including equity curves and important performance metrics such as Sharpe ratio, Sortino ratio, and maximum draw down of your test run.

<p align="center">
  <img src="https://github.com/MarkusMusch/bot/blob/main/images/single_strat_backtest.png">
</p>

### Unit Tests

To run the included unit tests execute

pytest-3 -v

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
