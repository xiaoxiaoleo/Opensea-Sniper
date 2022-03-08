import time
from typing import (
    Optional
)

from web3.types import TxParams, TxReceipt

from web3 import Web3

from core.chain_network import ChainNetwork
from core.eoa_account import EoaAccount
from core.common import TxHash
from core.common import Wei, Token, TokenWei, AddressType, GWei
from core.common import get_logger

logger = get_logger('account.log')



class ChainAddress():
    def __init__(self,
                 address: AddressType,
                 chain: ChainNetwork
                 ) -> None:
        self.chain = chain
        self.address = chain.w3.toChecksumAddress(address)

    def show_balance(self):
        balance: TokenWei = self.chain.w3.eth.get_balance(self.address)
        balance = balance / 10 ** 18
        logger.info(f"balance: {balance} Coin")

    def balance(self):
        balance: TokenWei = self.chain.w3.eth.get_balance(self.address)
        balance = balance / 10 ** 18
        #logger.info(f"balance: {balance} Coin")
        return Token(balance)

    def balance_wei(self):
        balance: TokenWei = self.chain.w3.eth.get_balance(self.address)
        logger.info(f"balance: {balance} Wei")
        return balance

class ChainAccount():
    def __init__(self,
                 account: EoaAccount,
                 chain: ChainNetwork
                 ) -> None:
        self.account = account
        self.chain = chain
        self.address = chain.w3.toChecksumAddress(account.address)

    def wait(self, hash: TxHash, timeout: int = 3600) -> TxReceipt:
        return self.chain.w3.eth.waitForTransactionReceipt(hash, timeout=timeout)

    def nonce(self):
        return self.chain.w3.eth.getTransactionCount(self.address)

    def sign(self,
             txn=None,  # transaction dict
             nonce: Optional[int] = None,
             gas_price: Optional[int] = None ) -> TxHash:
        if txn == {}:
            logger.error(f"Empty transaction params, skip")
            return [None, None]
        txn['chainId'] = self.chain.chain_id
        txn['from'] = self.address
        txn['gasPrice'] = Web3.toWei(gas_price, 'gwei') if gas_price is not None else Web3.toWei(self.chain.gas_price, 'gwei')
        txn['nonce'] = nonce if nonce is not None else self.chain.w3.eth.getTransactionCount(self.address)
        current_nonce = txn['nonce']
        logger.warn(f'{txn}')
        logger.warn(f'Sign in chain: {self.chain.chain_name}')
        logger.warn(f'Sign transaction using address: {self.account.address}')
        tx_signed = self.chain.w3.eth.account.sign_transaction(txn, private_key=self.account.private_key)
        return [tx_signed, current_nonce]

    def push(self, tx_signed, current_nonce) -> TxHash:
        tx_hash = self.chain.w3.eth.sendRawTransaction(tx_signed.rawTransaction)
        tx_hash = Web3.toHex(tx_hash)
        logger.info(
            (
                f"Pushed transaction {tx_hash} "
            )
        )
        timeout = 3600  # 1 hour
        timer_start = time.monotonic()
        self.wait(tx_hash, timeout)

        # NOTE: Wait for nonce to be incremented of for the timeout interval to run out.
        while (
                current_nonce == self.chain.w3.eth.getTransactionCount(self.address)
                and time.monotonic() - timer_start <= timeout
        ):
            time.sleep(0.5)

        logger.info(
            (
                f"Success transaction {tx_hash} "
            )
        )

    def push_no_wait(self, tx_signed) -> TxHash:
        tx_hash = self.chain.w3.eth.sendRawTransaction(tx_signed.rawTransaction)
        tx_hash = Web3.toHex(tx_hash)
        logger.info(
            (
                f"Pushed transaction {tx_hash} "
            )
        )

    def sign_and_push(self,
                      txn=None,  # transaction dict
                      nonce: Optional[int] = None,
                      gas_price: Optional[GWei] = None, ) -> TxHash:
        tx_signed, current_nonce = self.sign(txn=txn, nonce= nonce, gas_price = gas_price)
        if tx_signed is not None:
            self.push(tx_signed, current_nonce)

    def get_nonce(self):
        return self.chain.w3.eth.getTransactionCount(self.address)

    def show_balance(self):
        balance: TokenWei = self.chain.w3.eth.get_balance(self.account.address)
        balance = balance / 10 ** 18
        logger.info(f"balance: {balance} Coin")

    def balance(self):
        balance: TokenWei = self.chain.w3.eth.get_balance(self.account.address)
        balance = balance / 10 ** 18
        #logger.info(f"balance: {balance} Coin")
        return Token(balance)

    def balance_wei(self):
        balance: TokenWei = self.chain.w3.eth.get_balance(self.account.address)
        logger.info(f"balance: {balance} Wei")
        return balance



    def sendETH_nowait(self, to_address: AddressType, amount: Wei, gas: int = 21000, gas_price: GWei = None):
        logger.info(f'From {self.account.address} send ETH to {to_address}')
        to_address = self.chain.w3.toChecksumAddress(to_address)
        amount = Wei(amount)

        tx_param = self._get_tx_params(
            to_address=to_address,
            gas=gas,
            amount=amount,
            gas_price=Web3.toWei(gas_price, 'gwei') if gas_price is not None else Web3.toWei(self.chain.gas_price, 'gwei'),
        )

        logger.info(tx_param)
        self.sign_and_push_no_wait(tx_param)

    def sendETH_params(self, to_address: AddressType, amount: Wei, gas: int = 21000, gas_price: GWei = None):
        logger.info(f'From {self.account.address} send ETH to {to_address}')
        to_address = self.chain.w3.toChecksumAddress(to_address)
        amount = Wei(amount)

        tx_param = self._get_tx_params(
            to_address=to_address,
            gas=gas,
            amount=amount,
            gas_price=Web3.toWei(gas_price, 'gwei') if gas_price is not None else Web3.toWei(self.chain.gas_price, 'gwei'),
        )

        logger.info(tx_param)

        return tx_param

    def _get_tx_params(
            self,
            to_address: AddressType = None,
            amount: Wei = 0,
            gas: Optional[int] = None,
            gas_price: Optional[GWei] = None,
            nonce: Optional[int] = None,
    ) -> TxParams:

        return {
            'from': self.address,
            'value': amount,
            'to': to_address,
            'chainId': self.chain.chain_id,
            'gas': gas if gas is not None else self.tx_gas,
            'gasPrice': Web3.toWei(gas_price, 'gwei') if gas_price is not None else Web3.toWei(self.chain.gas_price, 'gwei'),
            'nonce': (
                nonce
                if nonce is not None
                else self.chain.w3.eth.getTransactionCount(self.address)
            ),
        }
