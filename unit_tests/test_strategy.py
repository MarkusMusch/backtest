from unittest.mock import patch

from src.Assets import btc_cont_1h
from src.RESTClient import BinanceFuturesClient
from src.strategies.ContinuationTrade import ContinuationTrade
from src.MarketStructure import MarketStructure


@patch('src.Strategy.requests.post')
def test_strategy_send_message(mock_post):
    """Test sending a message to Telegram."""

    ec = BinanceFuturesClient()

    ms = MarketStructure(btc_cont_1h.ath, btc_cont_1h.prev_low, btc_cont_1h.ath,
                         btc_cont_1h.prev_low)

    strategy = ContinuationTrade(ec, ms, btc_cont_1h, False, False)

    response = strategy._send_message('This is a test')

    assert response is not None


@patch('src.Strategy.TradeClient._place_order')
def test_strategy_long(mock_post):
    """Test executing a long trade on exchange."""

    ec = BinanceFuturesClient()

    ms = MarketStructure(btc_cont_1h.ath, btc_cont_1h.prev_low, btc_cont_1h.ath,
                         btc_cont_1h.prev_low)

    strategy = ContinuationTrade(ec, ms, btc_cont_1h, True, False)

    price = 19894
    risk = 0.01943

    strategy._long(price, risk)

    trade_size = min(btc_cont_1h.max_leverage*btc_cont_1h.initial_equity,
                     (btc_cont_1h.max_risk/risk) * btc_cont_1h.initial_equity)
    coins = round(trade_size/price, btc_cont_1h.decimals)

    assert strategy._position == coins
    assert strategy._equity == btc_cont_1h.initial_equity \
        - (1.+ec.taker_fees_USD_futures) * coins*price


@patch('src.Strategy.TradeClient._place_order')
def test_strategy_short(mock_post):
    """Test executing a long trade on exchange."""

    ec = BinanceFuturesClient()

    ms = MarketStructure(btc_cont_1h.ath, btc_cont_1h.prev_low, btc_cont_1h.ath,
                         btc_cont_1h.prev_low)

    strategy = ContinuationTrade(ec, ms, btc_cont_1h, True, False)

    price = 19894
    risk = 0.01943

    strategy._short(price, risk)

    trade_size = min(btc_cont_1h.max_leverage*btc_cont_1h.initial_equity,
                     (btc_cont_1h.max_risk/risk) * btc_cont_1h.initial_equity)
    coins = round(trade_size/price, btc_cont_1h.decimals)

    assert strategy._position == -coins
    assert strategy._equity == btc_cont_1h.initial_equity \
        + (1.-ec.taker_fees_USD_futures) * coins*price


@patch('src.Strategy.TradeClient._place_order')
def test_strategy_close_long(mock_post):
    """Test executing a long trade on exchange."""

    ec = BinanceFuturesClient()

    ms = MarketStructure(btc_cont_1h.ath, btc_cont_1h.prev_low, btc_cont_1h.ath,
                         btc_cont_1h.prev_low)

    strategy = ContinuationTrade(ec, ms, btc_cont_1h, True, False)

    price = 19894

    strategy._close_long_trade(price)

    assert strategy._position == 0
    assert strategy._equity == btc_cont_1h.initial_equity


@patch('src.Strategy.TradeClient._place_order')
def test_strategy_close_short(mock_post):
    """Test executing a short trade on exchange."""

    ec = BinanceFuturesClient()

    ms = MarketStructure(btc_cont_1h.ath, btc_cont_1h.prev_low, btc_cont_1h.ath,
                         btc_cont_1h.prev_low)

    strategy = ContinuationTrade(ec, ms, btc_cont_1h, True, False)

    price = 19894

    strategy._close_short_trade(price)

    assert strategy._position == 0
    assert strategy._equity == btc_cont_1h.initial_equity
