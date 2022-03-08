import sys

import time
from core.common import get_logger
from thirdparty.open_sea_v1.endpoints.client import ClientParams
from thirdparty.open_sea_v1.endpoints.orders import OrdersEndpoint
from thirdparty.open_sea_v1.endpoints.events import EventType, EventsEndpoint
from thirdparty.opensea.utils import get_order, putorder
from wconfig import OpenseaKey, ACCOUNT1


gasRate = 1.4
chain_name = 'eth'
buy_price = 0
asset_contract_address: str = '0x4db1f25d3d98600140dfc18deb7515be5bd293af'
account = ACCOUNT1


logger = get_logger('test.log')

def get_events():
    time_range = 3 # last 30 seconds orders
    client_params = ClientParams(
        api_key=OpenseaKey[0],
        offset=0,
        max_pages=1,
        limit=50
    )

    endpoint = EventsEndpoint(
        client_params=client_params,
        asset_contract_address=asset_contract_address,
        occurred_before=None,
        occurred_after=int(time.time()) - time_range,
        only_opensea=True,
        #auction_type='dutch',
        event_type=EventType.CREATED
    )

    flattened_events_pages: list = endpoint.get_parsed_pages()
    if len(flattened_events_pages) > 0:
        return flattened_events_pages
    else:
        logger.error(f'No event in last {time_range} second')



while True:
    flattened_events_pages = get_events()
    if flattened_events_pages:
        event = flattened_events_pages[0]
        price = event.starting_price
        if int(price) <= buy_price * 10**18:
            tokenid = event.asset.token_id
            order = get_order(asset_contract_address, tokenid)
            if order is None:
                continue
            order_status = putorder(chain_name, order, int(price), account, gasRate)
            if order_status:
                sys.exit()

    #time.sleep(0.5)
