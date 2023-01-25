import configparser
import os

import requests

def send_message(message: str):
    """Sends a message to a Telegram group."""

    config = configparser.ConfigParser()
    config.read(os.path.expanduser('~') + '/config.ini')

    bot_token = config['Telegram Dev']['bot_token']
    group_id = config['Telegram Dev']['group_id']

    params = {'chat_id': group_id, 'text': message, 'parse_mode': 'HTML'}
    requests.post('https://api.telegram.org/bot{}/sendMessage'
                  .format(bot_token), params)