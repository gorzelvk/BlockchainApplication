""" This file contains functions and tools required to create blockchain network """
import hashlib

GENESIS_HASH = '0' * 64
INITIAL_COIN_AMOUNT = 100000000.0
INITIAL_PRICE = 1.0
PRICE_LIST = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]


def compute_hash(*args) -> str:
    hashed_element = ''
    hash_result = hashlib.sha256()

    # hash each argument
    for arg in args:
        hashed_element += str(arg)

    hash_result.update(hashed_element.encode('utf-8'))
    return hash_result.hexdigest()


# Block is a basic container of information in blockchain
class Block:

    def __init__(self, number=0, previous_block_hash=GENESIS_HASH, data=None, nonce=0, timestamp=None):
        self.previous_block_hash = previous_block_hash
        self.data = data
        self.nonce = nonce
        self.number = number
        self.timestamp = timestamp

    def get_hash(self):
        self.hash = compute_hash(self.previous_block_hash, self.number, self.data, self.nonce, self.timestamp)
        return self.hash

    def get_previous_block_hash(self) -> str:
        return self.previous_block_hash

    def get_data(self) -> dict:
        return self.data

    def get_nonce(self) -> int:
        return self.nonce

    def get_timestamp(self) -> str:
        return self.timestamp

    def __str__(self) -> str:
        return str('\nBlock number: %s\nBlock hash: %s\nPrevious block hash: %s'
                   '\nBlock data: %s\nBlock nonce: %s\nBlock timestamp: %s' % (
                    self.number,
                    self.hash,
                    self.previous_block_hash,
                    self.get_data(),
                    self.get_nonce(),
                    self.get_timestamp()
                    ))


# Blockchain class is used to verify new blocks and to add them to the chain
class Blockchain:
    DIFFICULTY = 4

    def __init__(self):
        self.chain = []

    def add_block(self, block):
        self.chain.append(block)

    def remove_block(self, block):
        self.chain.remove(block)

    def mine_block(self, block):
        try:
            block.previous_block_hash = self.chain[-1].get_hash()
        except IndexError:
            pass

        while True:
            if block.get_hash()[:self.DIFFICULTY] == '0' * self.DIFFICULTY:
                self.add_block(block)
                break
            else:
                block.nonce += 1

    def is_blockchain_valid(self):
        newest_hash = self.chain[len(self.chain)-1].get_hash()  # current hash for current block
        for i in range(1, len(self.chain)):
            current_hash = self.chain[i-1].get_hash()  # current hash for previous block
            previous_hash = self.chain[i].get_previous_block_hash()  # previous hash for current block
            if previous_hash != current_hash or current_hash[:self.DIFFICULTY] != '0' * self.DIFFICULTY:
                return False
            if newest_hash[:self.DIFFICULTY] != '0' * self.DIFFICULTY:
                return False
        return True

