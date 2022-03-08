from core.chain_network import ChainNetwork
from core.contract import Contract
from core.common import TokenWei, AddressType
from core.common import load_abi
from wconfig import CONTRACT_ADDRESS, ZEROADDR
import time
from web3 import Web3
from hexbytes import HexBytes




class OpenseaContract(Contract):
    def __init__(self,
                 chain: ChainNetwork,
                 ) -> None:
        self.app_name = 'raca '
        self.address = chain.w3.toChecksumAddress(CONTRACT_ADDRESS[chain.chain_name]['opensea_ex'])
        self.chain = chain
        self.abi = load_abi('opensea_ex.json')
        self.contract = chain.w3.eth.contract(
            address=self.address,
            abi=self.abi
        )

    '''
    Function: Function: atomicMatch_(address[14] addrs, uint256[18] uints, uint8[8] feeMethodsSidesKindsHowToCalls, \
    bytes calldataBuy, bytes calldataSell, bytes replacementPatternBuy, bytes replacementPatternSell, bytes staticExtradataBuy,\
     bytes staticExtradataSell, uint8[2] vs, bytes32[5] rssMetadata)

    '''

    def atomicMatch_(self, from_addr, Order):
        # common_Address
        #Order
        if Order.maker['address'].lower() == from_addr.lower():
            self.logger.error('the seller is you')
            return {}

        buy_Exchange = Order.exchange
        buy_Maker = from_addr
        buy_Taker = Order.maker['address']
        buy_FeeRecipient = ZEROADDR
        buy_Target = Order.target
        buy_StaticTarget = ZEROADDR
        buy_PaymentToken = ZEROADDR
        sell_Exchange = Order.exchange
        sell_Maker = Order.maker['address']
        sell_Taker = ZEROADDR
        sell_FeeRecipient = Order.fee_recipient['address']
        sell_Target = Order.target
        sell_StaticTarget = ZEROADDR
        sell_PaymentToken = ZEROADDR

        # uint256_18_parameters
        buy_MakerRelayerFee = Order.maker_relayer_fee
        buy_TakerRelayerFee = Order.taker_relayer_fee
        buy_MakerProtocolFee = Order.maker_protocol_fee
        buy_TakerProtocolFee = Order.taker_protocol_fee
        buy_BasePrice = Order.base_price
        buy_Extra = Order.extra
        buy_ListingTime = int(time.time())
        buy_ExpirationTime = '0'
        buy_Salt = self.get_buysalt(Order.salt)
        sell_MakerRelayerFee = Order.maker_relayer_fee
        sell_TakerRelayerFee = Order.taker_relayer_fee
        sell_MakerProtocolFee = Order.maker_protocol_fee
        sell_TakerProtocolFee = Order.taker_protocol_fee
        sell_BasePrice = Order.base_price
        sell_Extra = Order.extra
        sell_ListingTime = Order.listing_time
        sell_ExpirationTime = Order.expiration_time
        sell_Salt = Order.salt

        # feeMethodsSidesKindsHowToCalls
        buy_FeeMethod = Order.fee_method
        buy_Side = 0
        buy_SaleKind = Order.sale_kind
        buy_HowToCall = Order.how_to_call
        sell_FeeMethod = Order.fee_method
        sell_Side = 0 if buy_Side else 1
        sell_SaleKind = Order.sale_kind
        sell_HowToCall = Order.how_to_call

        #
        _calldatabuy = Order.calldata[:10] + str(from_addr[2:].lower()).zfill(128) + Order.calldata[138:]
        calldataBuy = bytes.fromhex(_calldatabuy[2:])
        calldataSell = bytes.fromhex(Order.calldata[2:])

        #
        replacementPatternBuy  = bytes.fromhex(self.get_replacementPatternBuy(Order.replacement_pattern)[2:])
        replacementPatternSell = bytes.fromhex(Order.replacement_pattern[2:])

        #
        staticExtradataBuy = b''
        staticExtradataSell = b''

        #
        buySig_V = Order.v
        sellSig_V = Order.v

        buySig_R = Order.r
        buySig_S = Order.s
        sellSig_R = Order.r
        sellSig_S = Order.s
        metadata = '0x'

        common_Address = [Web3.toChecksumAddress(buy_Exchange),
                          Web3.toChecksumAddress(buy_Maker),
                          Web3.toChecksumAddress(buy_Taker),
                          Web3.toChecksumAddress(buy_FeeRecipient),
                          Web3.toChecksumAddress(buy_Target),
                          Web3.toChecksumAddress(buy_StaticTarget),
                          Web3.toChecksumAddress(buy_PaymentToken),
                          Web3.toChecksumAddress(sell_Exchange),
                          Web3.toChecksumAddress(sell_Maker),
                          Web3.toChecksumAddress(sell_Taker),
                          Web3.toChecksumAddress(sell_FeeRecipient),
                          Web3.toChecksumAddress(sell_Target),
                          Web3.toChecksumAddress(sell_StaticTarget),
                          Web3.toChecksumAddress(sell_PaymentToken)]

        uint256_18_parameters = [int(buy_MakerRelayerFee),
                                 int(buy_TakerRelayerFee),
                                 int(buy_MakerProtocolFee),
                                 int(buy_TakerProtocolFee),
                                 int(buy_BasePrice),
                                 int(buy_Extra),
                                 int(buy_ListingTime),
                                 int(buy_ExpirationTime),
                                 int(buy_Salt),
                                 int(sell_MakerRelayerFee),
                                 int(sell_TakerRelayerFee),
                                 int(sell_MakerProtocolFee),
                                 int(sell_TakerProtocolFee),
                                 int(sell_BasePrice),
                                 int(sell_Extra),
                                 int(sell_ListingTime),
                                 int(sell_ExpirationTime),
                                 int(sell_Salt)]

        feeMethodsSidesKindsHowToCalls = [
            buy_FeeMethod,
            buy_Side,
            buy_SaleKind,
            buy_HowToCall,
            sell_FeeMethod,
            sell_Side,
            sell_SaleKind,
            sell_HowToCall]

        vs = [
            int(buySig_V),
            int(sellSig_V)
        ]

        rssMetadata = [Web3.toBytes(hexstr=buySig_R),
                       Web3.toBytes(hexstr=buySig_S),
                       Web3.toBytes(hexstr=sellSig_R),
                       Web3.toBytes(hexstr=sellSig_S),
                       Web3.toBytes(hexstr=metadata)]

        func = self.contract.functions.atomicMatch_(addrs=common_Address, uints=uint256_18_parameters,
                                                    feeMethodsSidesKindsHowToCalls=feeMethodsSidesKindsHowToCalls,
                                                    calldataBuy=calldataBuy, calldataSell=calldataSell,
                                                    replacementPatternBuy=replacementPatternBuy,
                                                    replacementPatternSell=replacementPatternSell,
                                                    staticExtradataBuy=staticExtradataBuy,
                                                    staticExtradataSell=staticExtradataSell, vs=vs,
                                                    rssMetadata=rssMetadata)
        tx_param = self._build_tx(func, gas=500000)
        tx_param['value'] = int(Order.base_price)
        return tx_param

    '''
        function ordersCanMatch_(
        address[14] addrs,
        uint[18] uints,
        uint8[8] feeMethodsSidesKindsHowToCalls,
        bytes calldataBuy,
        bytes calldataSell,
        bytes replacementPatternBuy,
        bytes replacementPatternSell,
        bytes staticExtradataBuy,
        bytes staticExtradataSell)
    '''

    def ordersCanMatch_(self, from_addr  , Order):
        # common_Address
        #Order
        if Order.maker['address'].lower() == from_addr.lower():
            self.logger.error('the seller is you')
            return {}

        buy_Exchange = Order.exchange
        buy_Maker = from_addr
        buy_Taker = Order.maker['address']
        buy_FeeRecipient = ZEROADDR
        buy_Target = Order.target
        buy_StaticTarget = ZEROADDR
        buy_PaymentToken = ZEROADDR
        sell_Exchange = Order.exchange
        sell_Maker = Order.maker['address']
        sell_Taker = ZEROADDR
        sell_FeeRecipient = Order.fee_recipient['address']
        sell_Target = Order.target
        sell_StaticTarget = ZEROADDR
        sell_PaymentToken = ZEROADDR

        # uint256_18_parameters
        buy_MakerRelayerFee = Order.maker_relayer_fee
        buy_TakerRelayerFee = Order.taker_relayer_fee
        buy_MakerProtocolFee = Order.maker_protocol_fee
        buy_TakerProtocolFee = Order.taker_protocol_fee
        buy_BasePrice = Order.base_price
        buy_Extra = Order.extra
        buy_ListingTime = int(time.time())
        buy_ExpirationTime = '0'
        buy_Salt = self.get_buysalt(Order.salt)
        sell_MakerRelayerFee = Order.maker_relayer_fee
        sell_TakerRelayerFee = Order.taker_relayer_fee
        sell_MakerProtocolFee = Order.maker_protocol_fee
        sell_TakerProtocolFee = Order.taker_protocol_fee
        sell_BasePrice = Order.base_price
        sell_Extra = Order.extra
        sell_ListingTime = Order.listing_time
        sell_ExpirationTime = Order.expiration_time
        sell_Salt = Order.salt

        # feeMethodsSidesKindsHowToCalls
        buy_FeeMethod = Order.fee_method
        buy_Side = 0
        buy_SaleKind = Order.sale_kind
        buy_HowToCall = Order.how_to_call
        sell_FeeMethod = Order.fee_method
        sell_Side = 0 if buy_Side else 1
        sell_SaleKind = Order.sale_kind
        sell_HowToCall = Order.how_to_call

        #
        _calldatabuy = Order.calldata[:10] + str(from_addr[2:].lower()).zfill(128) + Order.calldata[138:]
        calldataBuy = bytes.fromhex(_calldatabuy[2:])
        calldataSell = bytes.fromhex(Order.calldata[2:])

        #
        replacementPatternBuy  = bytes.fromhex(self.get_replacementPatternBuy(Order.replacement_pattern)[2:])
        replacementPatternSell = bytes.fromhex(Order.replacement_pattern[2:])

        #
        staticExtradataBuy = b''
        staticExtradataSell = b''

        common_Address = [Web3.toChecksumAddress(buy_Exchange),
                          Web3.toChecksumAddress(buy_Maker),
                          Web3.toChecksumAddress(buy_Taker),
                          Web3.toChecksumAddress(buy_FeeRecipient),
                          Web3.toChecksumAddress(buy_Target),
                          Web3.toChecksumAddress(buy_StaticTarget),
                          Web3.toChecksumAddress(buy_PaymentToken),
                          Web3.toChecksumAddress(sell_Exchange),
                          Web3.toChecksumAddress(sell_Maker),
                          Web3.toChecksumAddress(sell_Taker),
                          Web3.toChecksumAddress(sell_FeeRecipient),
                          Web3.toChecksumAddress(sell_Target),
                          Web3.toChecksumAddress(sell_StaticTarget),
                          Web3.toChecksumAddress(sell_PaymentToken)]

        uint256_18_parameters = [int(buy_MakerRelayerFee),
                                 int(buy_TakerRelayerFee),
                                 int(buy_MakerProtocolFee),
                                 int(buy_TakerProtocolFee),
                                 int(buy_BasePrice),
                                 int(buy_Extra),
                                 int(buy_ListingTime),
                                 int(buy_ExpirationTime),
                                 int(buy_Salt),
                                 int(sell_MakerRelayerFee),
                                 int(sell_TakerRelayerFee),
                                 int(sell_MakerProtocolFee),
                                 int(sell_TakerProtocolFee),
                                 int(sell_BasePrice),
                                 int(sell_Extra),
                                 int(sell_ListingTime),
                                 int(sell_ExpirationTime),
                                 int(sell_Salt)]

        feeMethodsSidesKindsHowToCalls = [
            buy_FeeMethod,
            buy_Side,
            buy_SaleKind,
            buy_HowToCall,
            sell_FeeMethod,
            sell_Side,
            sell_SaleKind,
            sell_HowToCall]



        ordercanmatch = self.contract.functions.ordersCanMatch_(addrs=common_Address, uints=uint256_18_parameters,
                                                    feeMethodsSidesKindsHowToCalls=feeMethodsSidesKindsHowToCalls,
                                                    calldataBuy=calldataBuy, calldataSell=calldataSell,
                                                    replacementPatternBuy=replacementPatternBuy,
                                                    replacementPatternSell=replacementPatternSell,
                                                    staticExtradataBuy=staticExtradataBuy,
                                                    staticExtradataSell=staticExtradataSell ).call()
        #ordercanmatch
        #tx_param = self._build_tx(func, gas=0)
        #tx_param['value'] = int(Order.base_price)
        #if not ordercanmatch:
        #    self.logger.error(f" can not match in contract")
        return ordercanmatch


    @staticmethod
    def get_buysalt(buy_salt):
        if len(buy_salt) < 77:
            buy_salt = buy_salt + '1'* (77-len(buy_salt))
        else:
            buy_salt = int(buy_salt) - 1
        return buy_salt

    @staticmethod
    def get_replacementPatternBuy(replacementPatternSell):
        arg_0 = replacementPatternSell[:10]
        arg_1 = replacementPatternSell[10:74]
        arg_2 = replacementPatternSell[74:138]
        arg_3 = replacementPatternSell[138:]
        return arg_0+arg_2+arg_1+arg_3