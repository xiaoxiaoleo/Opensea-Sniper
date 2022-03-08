from core.contract import Contract
from core.common import Token, TokenWei, AddressType, MAX_APPROVAL_INT
from core.common import load_abi


class ERC721Contract(Contract):
    def __init__(self,
                 chain,
                 address
                 ) -> None:
        self.address = chain.w3.toChecksumAddress(address)
        self.chain = chain
        self.abi = load_abi('ERC721.json')
        self.contract = chain.w3.eth.contract(
            address=chain.w3.toChecksumAddress(self.address),
            abi=self.abi
        )
        #self.token_symbol = self.contract.functions.symbol().call()
        #self.token_decimals = self.contract.functions.decimals().call()
    #
    # def token_info(self):
    #     self.logger.info(
    #         f'token name {self.token_symbol} \t token decimal {self.token_decimals} \t token addr {self.address}')
    #
    # def _token_multiply_decimal(self, amount: Token) -> TokenWei:
    #     return TokenWei(amount * (10 ** self.token_decimals))
    #
    # def _token_devide_decimal(self, amount: TokenWei) -> Token:
    #     return Token(amount / (10 ** self.token_decimals))

    def safeTransferFrom(self, from_address, to_address, tokenId, value, gas=None):
        if not gas:
            gas = 200000
        from_address = self.chain.w3.toChecksumAddress(from_address)
        to_address = self.chain.w3.toChecksumAddress(to_address)
        value=int(value)
        tokenId=int(tokenId)
        data = '0x'
        func = self.contract.functions.safeTransferFrom(from_address, to_address, tokenId, value, data)
        tx_param = self._build_tx(func, gas=gas)
        return tx_param

    def transferFrom(self, from_address, to_address, nftid, gas=None):
        if not gas:
            gas = 150000
        from_address = self.chain.w3.toChecksumAddress(from_address)
        to_address = self.chain.w3.toChecksumAddress(to_address)
        nftid=int(nftid)
        func = self.contract.functions.transferFrom(from_address, to_address, nftid)
        tx_param = self._build_tx(func, gas=gas)
        return tx_param




    def mint(self, amount, gas=None):
        if not gas:
            gas = 600000
        amount=int(amount)
        func = self.contract.functions.mint(amount)
        tx_param = self._build_tx(func, gas=gas)
        return tx_param

    def isApprovedForAll(
            self,
            from_address: AddressType = None,
            approve_to: AddressType = None,
    ) -> bool:
        approve_to = self.chain.w3.toChecksumAddress(approve_to)
        from_address = self.chain.w3.toChecksumAddress(from_address)

        status = self.contract.functions.isApprovedForAll(
            from_address, approve_to
        ).call()
        self.logger.info(f"approved {status}")

        return status


    def setApprovalForAll(self, to_address, gas=None):
        to_address = self.chain.w3.toChecksumAddress(to_address)
        if not gas:
            gas = 100000
        _approved = 1
        func = self.contract.functions.setApprovalForAll(to_address, _approved)
        tx_param = self._build_tx(func, gas=gas)
        return tx_param


    def cancalApproval(self, to_address, gas=None):
        to_address = self.chain.w3.toChecksumAddress(to_address)
        if not gas:
            gas = 100000
        _approved = 0
        func = self.contract.functions.setApprovalForAll(to_address, _approved)
        tx_param = self._build_tx(func, gas=gas)
        return tx_param


    def ownerOf(self, tokenid):
        tokenid = int(tokenid)
        address = self.contract.functions.ownerOf(tokenid).call()
        return address