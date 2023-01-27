from src.Assets import Asset, Params, TradeData
from src.strategies.ContinuationTrade import ContinuationTrade
from src.MarketStructure import MarketStructure


def test_strategy_long():
    """Test executing a long trade on exchange."""

    strategy = ContinuationTrade()

    ms = MarketStructure((1, 1), (1, 1), (1, 1), (1, 1))
    asset = Asset('BTCBUSD', 3, ms)
    params = Params(0.02, 2, 2, '1h')
    trade_data = TradeData(0.0)

    price = 19894
    risk = 0.01943

    strategy._long(price, risk, asset, params, trade_data)

    trade_size = (0.02/risk) * 100
    coins = round(trade_size/price, 3)

    assert trade_data.position == coins
    assert trade_data.equity == 100 - coins*price


def test_strategy_short():
    """Test executing a long trade on exchange."""

    strategy = ContinuationTrade()

    ms = MarketStructure((1, 1), (1, 1), (1, 1), (1, 1))
    asset = Asset('BTCBUSD', 3, ms)
    params = Params(0.02, 2, 2, '1h')
    trade_data = TradeData(0.0)

    price = 19894
    risk = 0.01943

    strategy._short(price, risk, asset, params, trade_data)

    trade_size = (0.02/risk) * 100
    coins = round(trade_size/price, 3)

    assert trade_data.position == -coins
    assert trade_data.equity == 100 + coins*price


def test_strategy_close_long():
    """Test executing a long trade on exchange."""

    strategy = ContinuationTrade()

    trade_data = TradeData(0.0)

    price = 19894

    strategy._close_long_trade(price, trade_data)

    assert trade_data.position == 0
    assert trade_data.equity == 100


def test_strategy_close_short():
    """Test executing a short trade on exchange."""

    strategy = ContinuationTrade()

    trade_data = TradeData(0.0)

    price = 19894

    strategy._close_short_trade(price, trade_data)

    assert trade_data.position == 0
    assert trade_data.equity == 100
