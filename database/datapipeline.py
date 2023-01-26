import configparser
import os
import sys

from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from RESTClient import BinanceFuturesClient
from DataHandler import DataHandler
from src.Assets import Timeframes


def download(market: str, timeframe: str, delta: timedelta):

    ec = BinanceFuturesClient()
    dh = DataHandler(vd=False)

    df = dh.aggregate_data(ec, market, timeframe,
                           datetime(2017, 7, 14, 0, 0, 0, 0),
                           delta)

    path = './database/datasets/binance_futures/' + market + '/'
    if not os.path.exists(path):
        os.makedirs(path)

    df.to_csv(path + timeframe + '.csv')


def compute_vds():
    markets = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'DOGEUSDT']

    for market in markets:

        df = pd.read_csv(market + '_1h.csv')
        dh = DataHandler(vd=False)

        df = dh._compute_vd(df)
        df = dh._compute_vd_ma(df, 2400)
        df = dh._compute_cvd(df)

        df.to_csv(market + '_1h.csv')


def plot_vdma():
    markets = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'DOGEUSDT']

    for market in markets:
        df = pd.read_csv(market + '_1h.csv')

        fig, ax = plt.subplots()

        df['datetime'] = pd.to_datetime(df['open time'], unit='ms')

        ax.plot(np.array(df['datetime']), np.array(df['close']), color='red')
        ax2 = ax.twinx()
        ax2.plot(np.array(df['datetime']),
                 np.array(df['volume_delta_moving_average_base_asset']))
        plt.show()


def plot_cvd():
    markets = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'DOGEUSDT']

    for market in markets:

        df = pd.read_csv(market + '_1h_spot.csv')

        fig, ax = plt.subplots()

        df['datetime'] = pd.to_datetime(df['open time'], unit='ms')

        ax.plot(np.array(df['datetime']), np.array(df['close']), color='red')
        ax2 = ax.twinx()
        ax2.plot(np.array(df['datetime']), np.array(df['cvd_quote_asset']))
        plt.show()


# usdt_markets = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'DOGEUSDT']
busd_markets = ['BTCBUSD', 'ETHBUSD', 'BNBBUSD', 'SOLBUSD', 'DOGEBUSD',
                'LTCBUSD', 'LINKBUSD', 'XRPBUSD', 'MATICBUSD']
#markets = ['LTCBUSD', 'LINKBUSD', 'XRPBUSD', 'MATICBUSD']
"""
for market in markets:
    download(market, Timeframes.ONE_DAY.value, timedelta(days=999))
    print(Timeframes.ONE_DAY.value + ' done! \n')
    download(market, Timeframes.FOUR_HOURS.value, timedelta(hours=3999))
    print(Timeframes.FOUR_HOURS.value + ' done! \n')
    download(market, Timeframes.ONE_HOUR.value, timedelta(hours=999))
    print(Timeframes.ONE_HOUR.value + ' done! \n')
    download(market, Timeframes.THIRTY_MINUTES.value,
             timedelta(minutes=29999))
    print(Timeframes.THIRTY_MINUTES.value + ' done! \n')
    download(market, Timeframes.FIFTEEN_MINUTES.value,
             timedelta(minutes=14999))
    print(Timeframes.FIFTEEN_MINUTES.value + ' done! \n')
    download(market, Timeframes.FIVE_MINUTES.value, timedelta(minutes=4999))
    print(Timeframes.FIVE_MINUTES.value + ' done! \n')
    print(market, ' done! \n')
"""

for test in ['test']:
    config = configparser.ConfigParser()
    config.read(os.path.expanduser('~') + '/config.ini')

    bot_token = config['Telegram Dev']['bot_token']
    group_id = config['Telegram Dev']['group_id']

    params = {'chat_id': group_id, 'text': test + 'done!', 
              'parse_mode': 'HTML'}
    response = requests.post('https://api.telegram.org/bot{}/sendMessage'
                             .format(bot_token), params)

for market in busd_markets:
    download(market, '1m', timedelta(minutes=999))

    config = configparser.ConfigParser()
    config.read(os.path.expanduser('~') + '/config.ini')

    bot_token = config['Telegram Dev']['bot_token']
    group_id = config['Telegram Dev']['group_id']

    params = {'chat_id': group_id, 'text': market + ' done!', 
              'parse_mode': 'HTML'}
    response = requests.post('https://api.telegram.org/bot{}/sendMessage'
                             .format(bot_token), params)

# compute_vds()
# plot_vdma()
# plot_cvd()


config = configparser.ConfigParser()
config.read(os.path.expanduser('~') + '/config.ini')

bot_token = config['Telegram Dev']['bot_token']
group_id = config['Telegram Dev']['group_id']

params = {'chat_id': group_id, 'text': 'Download Finished!', 
          'parse_mode': 'HTML'}
response = requests.post('https://api.telegram.org/bot{}/sendMessage'
                         .format(bot_token), params)