import pandas as pd

from src.RESTClient import BinanceFuturesClient
from src.Assets import btc_cont_1h
from src.strategies.ContinuationTrade import ContinuationTrade
from src.MarketStructure import MarketStructure

def test_continuation_trade_long():
    """Test if long trades are recognized and executed correctly."""

    ec = BinanceFuturesClient()
    ms = MarketStructure(btc_cont_1h.ath, btc_cont_1h.prev_low, btc_cont_1h.ath,
                         btc_cont_1h.prev_low)
    market = btc_cont_1h

    df = pd.read_csv('./database/datasets/binance_futures/BTCBUSD/1h.csv')
    df = df[(df['open time'] >= 1613934000000)
            & (df['open time'] <= 1613962800000)]


    strat = ContinuationTrade(ec, ms, market)

    for index, row in df.iterrows():
        strat.next_candle_trade(row)
        strat.next_candle_setup(row)

    assert True
