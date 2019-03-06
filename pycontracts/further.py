from pycontracts import contracts
from pycontracts.forward import Forward
from web3 import Web3

class Further(Forward):
    def __init__(self, w3, address):
        super().__init__(address)
        self.w3 = w3

    @staticmethod
    def wrap(w3, address):
        return Further(w3, address)


    @staticmethod
    def deploy(w3, owner, originator):
        def push(bs):
            return bytes(0x60 + len(bs)) + bs

        init = push(Web3.toBytes(hexstr=owner)) + contracts['further']['deploy']

        tx_hash = w3.eth.sendTransaction({
            'from': originator,
            'data': init,
        })
        r = w3.eth.waitForTransactionReceipt(tx_hash)
        return Further.wrap(w3, r.contractAddress)

    @property
    def owner(self):
        raise NotImplementedError

    def nonce(self):
        raise NotImplementedError

    def sign(self, private_key, target, value, data, nonce):
        raise NotImplementedError

    def transact(self, private_key, originator, target = None, value = 0, data = b'', nonce = None):
        self.w3.eth.sendTransaction({
            'to': self.address,
            'from': originator,
            'value': value,
        })
