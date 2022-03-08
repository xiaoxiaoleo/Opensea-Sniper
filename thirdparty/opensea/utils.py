from core.common import get_logger
from contracts.opensea import OpenseaContract
from core.chain_account import ChainAccount
from core.chain_network import ChainNetwork
from contracts.erc721 import ERC721Contract
from thirdparty.open_sea_v1.endpoints.client import ClientParams
from thirdparty.open_sea_v1.endpoints.orders import OrdersEndpoint
from thirdparty.open_sea_v1.endpoints.assets import AssetsEndpoint
from thirdparty.blocknative.gas import get_gasPrice
from wconfig import OpenseaKey

logger = get_logger('openseas.log')


def get_assets(asset_contract_address):
    logger.info(f"get assets")
    time_range = 30 # last 30 seconds orders
    client_params = ClientParams(
        api_key=OpenseaKey[1],
        offset=0,
        max_pages=1,
        limit=50
    )

    endpoint = AssetsEndpoint(
        client_params=client_params,
        asset_contract_address=asset_contract_address,
        order_by='sale_price',
        order_direction='asc'
    )

    flattened_events_pages: list = endpoint.get_parsed_pages()
    if len(flattened_events_pages) > 0:
        return flattened_events_pages
    else:
        logger.error('zero assets')
        return None

def get_order(asset_contract_address, token_id):
    logger.info(f'get order for token id {token_id}')
    client_params = ClientParams(
        api_key=OpenseaKey[0],
        limit=50,
        max_pages=1)

    endpoint = OrdersEndpoint(
        sale_kind=0,
        side=1,
        is_english=False,
        include_bundled=False,
        client_params=client_params,
        asset_contract_address=asset_contract_address,
        token_ids=[str(token_id)],
        order_by='eth_price',
        order_direction='asc',
        #listed_after=int(time.time() - 600)

    )

    test = endpoint.get_parsed_pages(flat=True)
    if len(test) > 0:
        return test[0]
    else:
        logger.error(f'no order for token id {token_id} ')
        return None
#order = test[0]

def verify_sale_balance(order, chain):

    erc721 = ERC721Contract(chain=chain, address=order.target)
    if erc721.ownerOf(order.asset.token_id).lower() == order.maker['address'].lower():
        return True
    else:
        return False



def putorder(chain_name, order, max_price, account, gasRate: float = None, gas_price: int = None ):
    chain = ChainNetwork(chain_name)
    if not verify_sale_balance(order, chain):
        logger.error(f'owner {order.maker["address"]} balance is zero, have sold.')
    order_price = int(order.base_price) /10**18
    if order_price <= max_price:
        logger.info(f"order price : {order_price}")
        gas_price = get_gasPrice() *  gasRate if gasRate else gas_price
        #my_account = ACCOUNT_530b
        chain_account = ChainAccount(account, chain)
        opensea = OpenseaContract(chain=chain)
        if True: #opensea.ordersCanMatch_(from_addr=account.address, Order=order):
            tx_params = opensea.atomicMatch_(from_addr=account.address, Order=order)
            print(tx_params)
            chain_account.sign_and_push(txn=tx_params, gas_price=gas_price)
            return True
        else:
            logger.info(f'order can not match in contract')
            return False
    else:
        logger.error(f' price change or high than max price {max_price} !')

        return False