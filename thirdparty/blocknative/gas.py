import requests
import json
import time

from core.chain_network import ChainNetwork

chain = ChainNetwork(chain_name='eth')

def getblocknum():
    block = chain.get_last_block()
    chain.get_last_block_time()
    print(block.number)

def get_gasPrice():
    API_URL = "https://api.blocknative.com/gasprices/blockprices?confidenceLevels=99"
    headers = {'Content-type': 'application/json',
               "Authorization": "27a476fd-e98c-4469-a8b8-552b00b519c7",
               'Accept': 'application/json, text/plain, */*',
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language':'en,zh-CN;q=0.9,zh;q=0.8',
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36'}
    r = requests.get(API_URL, headers=headers)

    if True:
        data = json.loads(r.text)
        if data.get('blockPrices'):
            gas = data['blockPrices'][0]['estimatedPrices']
            return int(gas[0]['price'])

        time.sleep(1)
        print(json.loads(r.text))

#
#
# while True:
#     getblocknum()
#     gasprice = postsign()
#     print(gasprice)
