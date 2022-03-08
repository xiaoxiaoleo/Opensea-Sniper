import locale
import logging
from dataclasses import dataclass

from thirdparty.open_sea_v1.helpers.ether_converter import EtherConverter, EtherUnit
from thirdparty.open_sea_v1.responses.abc import BaseResponse
from thirdparty.open_sea_v1.responses.asset import AssetResponse

logger = logging.getLogger(__name__)


@dataclass
class EventResponse(BaseResponse):
    _json: dict

    def __str__(self) -> str:
        locale.setlocale(locale.LC_ALL, '')  # big number str formater

        name = self.asset.name[:20]
        transaction_date = f"{self.transaction['timestamp'][:10]} {self.transaction['timestamp'][11:-3]}" if self.transaction else ''

        usd_price = round(self.usd_price / int(self.quantity), 2)
        usd_price = f"{usd_price:,.2f}"
        usd_price = f"{usd_price} USD"
        eth_price = self.eth_price / int(self.quantity)
        eth_price = f"{eth_price:.4f} ETH"  # trailing zeros

        str_representation = "    ".join([name, transaction_date, usd_price, eth_price])
        return str_representation

    def __post_init__(self):
        self.approved_account = self._json['approved_account']
        self.asset_bundle = self._json['asset_bundle']
        self.auction_type = self._json['auction_type']
        self.collection_slug = self._json['collection_slug']
        self.contract_address = self._json['contract_address']
        self.created_date = self._json['created_date']
        self.custom_event_name = self._json['custom_event_name']
        self.dev_fee_payment_event = self._json['dev_fee_payment_event']
        self.duration = self._json['duration']
        self.ending_price = self._json['ending_price']
        self.event_type = self._json['event_type']
        self.from_account = self._json['from_account']
        self.id = str(self._json['id'])
        self.owner_account = self._json['owner_account']
        self.quantity = self._json['quantity']
        self.starting_price = self._json['starting_price']
        self.to_account = self._json['to_account']
        self.total_price = self._json['total_price']
        self.bid_amount = self._json['bid_amount']
        self.is_private = self._json.get('is_private')

    @property
    def eth_price(self) -> float:
        if not self.total_price:
            logger.debug(f'Event {self.id} for asset {self.asset.name} ({self.asset.id}) has no ETH price. Returning 0.')
            return 0.0
        eth_price = EtherConverter(quantity=self.total_price, unit=EtherUnit.WEI).ether
        return eth_price

    @property
    def usd_price(self):
        if not self.payment_token:
            logger.debug(f'Event {self.id} for asset {self.asset.name} ({self.asset.id}) has no payment token. Returning 0.')
            return 0.0
        eth_to_usd_price = float(self.payment_token['usd_price'])  # 'eth_price' key also available
        usd_price = round(self.eth_price * eth_to_usd_price, 2)
        return usd_price

    @property
    def asset(self) -> AssetResponse:
        return AssetResponse(self._json['asset'])

    @property
    def payment_token(self) -> dict:
        return self._json['payment_token']

    @property
    def seller(self) -> dict:
        return self._json['seller']

    @property
    def transaction(self) -> dict:
        return self._json['transaction']

    @property
    def winner_account(self) -> dict:
        return self._json['winner_account']
