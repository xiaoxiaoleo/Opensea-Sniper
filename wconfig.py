import os
import logging
from core.chain_account import EoaAccount


env_dist = os.environ

DATA_PATH = env_dist.get('DATA_PATH') if env_dist.get('DATA_PATH') else "data"
LOG_PATH = env_dist.get('LOG_PATH') if env_dist.get('LOG_PATH') else f"/tmp/"


LOG_LEVEL = logging.DEBUG


MoralisKey = ['xxx']

CHAIN_PROVIDER = {
    "eth":'https://api.mycryptoapi.com/eth', }

OpenseaKey = ['30b9b2312343552f9442f24b8']
ACCOUNT1   = EoaAccount('address', 'privatekey')


HTTP_PROXY_URL = ''