from typing import (
    Callable,
    Dict,
    Optional,
)

from core.common import Wei, EmptyAddress
from core.common import get_logger

import json
from web3 import Web3
from web3.auto import w3 as neww3

class Contract:
    contract = None
    abi = None
    address = None
    chain = None
    test = 1
    logger = get_logger('contract.log')

    # def _get_tx_params(
    #         self,
    #         amount: Wei = 0,
    #         gas: Optional[int] = None,
    # ) -> TxParams:
    #     return {
    #         'from': EmptyAddress,
    #         'value': amount,
    #         'gas': gas if gas is not None else self.tx_gas,
    #         'gasPrice': 0,
    #         'nonce':  0
    #     }

    def _build_tx(self, func: Callable,
                  amount: Wei = 0,
                  gas: Optional[int] = None, ) -> Dict:
        params = {
            'from': EmptyAddress,
            'value': amount,
            'gas': gas if gas is not None else self.tx_gas,
            'gasPrice': 0,
            'nonce': 0
        }

        tx = func.buildTransaction(params)
        return tx

    def _build_diy_tx(self, to_address, data: str, value: Optional[int] = None,
                  gas: Optional[int] = None, ) -> Dict:

        tx =  {'chainId': 0,
               'from': EmptyAddress,
               'value': value if value is not None else 0,
               'gas': gas,
               'gasPrice': 0,
               'nonce': 0,
               'to': to_address,
               'data': data }
        return tx

    def show_all_fun(self):
        for fun_obj in self.contract.abi:
            if fun_obj.get('name'):
                funstr = f"{fun_obj['name']}("
                for j in fun_obj['inputs']:
                    funstr = funstr + j['internalType'] + ','
                funstr = funstr[:-1] + ')'
                #self.logger.info(funstr)
                select_hash = self.calc_selector(funstr)
                self.logger.info(f"{fun_obj['name']}\t{funstr}\t {select_hash}")


    @staticmethod
    def calc_selector(signature: str = "transfer(address,uint256)"):
        selector = Web3.keccak(text=signature).hex()[:10]
        #self.logger.info(f"signature: {signature} : selector {selector}")
        return selector

    def balance(self):
        return self.chain.w3.eth.get_balance(self.address)/10**18

    def show_address(self):
        self.logger.info(f"contract address {self.address}")

    def decode_input(self, input_data):
        contract = neww3.eth.contract(address=self.address, abi=self.abi)
        func_obj, func_params = contract.decode_function_input(input_data)

        print(func_params)