from web3 import Web3, HTTPProvider, TestRPCProvider
from web3.contract import Contract
from eth_keys import keys

from pycontracts import contracts

from binascii import unhexlify
from glob import glob
import os
import random

target = os.getenv("GANACHE_TARGET")
w3 = Web3(HTTPProvider(target))

def address(pk):
    if not isinstance(pk, keys.PrivateKey):
        pk = keys.PrivateKey(pk)
    return pk.public_key.to_checksum_address()

class Faucets:
    def __init__(self):
        self.keys = map(lambda f: unhexlify(f), [
            "e2ee547be17ac9f7777d4763c43fd726c0a2a6d40450c92de942d7925d620b6d",
            "0740fb09781e8fa771edcf1bddee93ad6772593b3139f1cf36b0d095d235887b",
            "ac72e464dac0448a28fa71b34bfe46b2356fe09bd4f5a73519ee60b3b92b9dab",
            "230eda6cc73da415d3b327426dde475a786bb5a0aeae2ca531aaaa8c0218a7a5",
            "91e3179925ef60e4d1f4daf0e7d67bdb5cf74ff3d456db0eb239e432290db31c",
            "66769c67a372926b945262a1c86b7944a669dbeab3d89771d7af691b3bfb20d8",
            "af40a15c4d369cdb39d01148d7b5f5dd4f9825447fabcbfc15e230db84fcb88b",
            "4ad882b7e0b24fd01ad6d2f281d469edb9d2bef2c2ee8871099c5fd7c7018317",
            "9042fc069b6abe8210d31195b382b61c3ee9149223fcb181016a49ba61a14d84",
            "bf32730f2b240c0c482126ecc1e2219554f3c738f19bd592e3ccf4cc005ddc1e",
        ])

        self.addresses = list(map(address, self.keys))

    def random(self):
        return random.choice(self.addresses)

    def ether(self, to, amount):
        w3.eth.sendTransaction({
            "from": self.random(),
            "to": to,
            "value": amount,
        })

faucets = Faucets()

def deploy(contract, faucet = None):
    tx_hash = w3.eth.sendTransaction({
        'from': faucet or faucets.random(),
        'data': contract['code']
    })
    r = w3.eth.waitForTransactionReceipt(tx_hash)
    if 'abi' in contract:
        return w3.eth.contract(r.contractAddress, abi = contract.get('abi'))
    else:
        return w3.eth.contract(r.contractAddress)
