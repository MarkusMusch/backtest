# Backtest

This is a spin off of the [bot](https://github.com/MarkusMusch/bot) repository focusing solely on the backtesting engine.

## Includes:

1. **Building your own backtests**

	* A ready-to-use backtest for an example strategy, making it easy to get started with backtesting your own strategies.

2. **Training your model**

	* The Backtest class serves as a template for backtesting, making it easy to plug in your own strategies and see how they would have fared under different market conditions in the past. It provides a train and a test method making it easy to do parameter optimizations and test the results for validity.

3. **Testing your model**

	* Backtest reports for the example strategy that provide a comprehensive overview of the strategy's performance, including plots of the equity curve and important performance metrics for different parameters.

	<p align="center">
	<img src="https://github.com/MarkusMusch/backtest/blob/main/images/BTCBUSD_1h.png" />
	</p>

    > The backtest in the image above shows the return curve optimized for maximal Sharpe ratio on the first 75% of the data and the equity curve of the same strategy on the test data together with the median and 90% confidence interval of 250 samples bootstraped from the returns of the optimal strategy in the training data. On the right hand side a table with performance metrics for the equity curve on the test data is being shown.

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

We utilize the Strategy Design Pattern to provide a unified interface for applying different trading strategies in backtests. The actual logic of each individual trading strategy is implemented in a derived class of the interface and therefore easily interchangeable. For this purpose, we implement an abstract class called "Strategy", that only implements the methods that all strategies have in common, namely ```_long```, ```_short```, ```_close_long_trade``` and ```_close_short_trade```. At the same time, it also provides two abstract methods ```next_candle_setup``` and ```next_candle_trade``` that provide the interface for users of this class, which have to be implemented by each derived class.

Our example is a strategy that bets on the continuation of an ongoing trend. If the market is in an up-trend, and certain criteria are met, the strategy enters a long trade to profit from the continuation of the up-trend. In the same way, we enter a short trade if the market is in an ongoing down-trend.

Whilst the abstract strategy class is in the backtest/src/ directory, the actual implementation of a particular strategy is in the backtest/src/strategies directory. 

So, to implement our trend continuation strategy, we create a new file in the backtest/src/strategies/ directory. In our case it is called ContinuationTrade.py. In this file we implement the trade logic in a class that inherits from Strategy.

<p align="center">
  <img src="https://github.com/MarkusMusch/backtest/blob/main/images/Strategy_UML.png"
  width=50%>
</p>

The Strategy base class has a two abstract methods that we have to implement in our child class.

The ```next_candle_setup``` and ```next_candle_trade``` methods give a public interface for our backtest modules.

The ```execute_trade``` method checks if a new trigger has been set or if there is an existing position and calls the ```entry_long```, ```entry_short```, ```exit_long```, or ```exit_short``` method respectively.

If ```entry_long``` or ```entry_short``` is being called some more conditions such as a sufficient reward/risk ratio are being checked. If those conditions are satisfied a trade is being entered on exchange via our RESTClient object for live trading, or recorded without actual execution for backtesting.

If ```exit_long``` or ```exit_short``` is being called the current trade is being closed on exchange via our RESTClient object for live trading, or recorded without actual execution for backtesting.


<p align="center">
<img src="https://github.com/MarkusMusch/backtest/blob/main/images/strategy_control_flow.png" />
</p>

This diagram shows the whole control flow described above.

### Writing Backtests

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
The Backtest object will also save a report of you backtest in the backtest/src/backtest_reports/ directory including equity curves and important performance metrics such as Sharpe ratio, Sortino ratio, and maximum draw down of your test run.

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
