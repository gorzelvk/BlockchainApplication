""" This file contains functions and tools required to create blockchain network """
import hashlib
import itertools
from typing import Optional
from datetime import datetime

GENESIS_HASH = '0' * 64


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
    hash = None
    previous_block_hash = GENESIS_HASH
    data = None
    nonce = 0
    number = None
    new_block_number = itertools.count()

    def __init__(self, data):
        self.data = data
        self.number = next(Block.new_block_number) + 1
        self.timestamp = datetime.now()

    def get_hash(self):
        self.hash = compute_hash(self.previous_block_hash, self.number, self.data, self.nonce)
        return self.hash

    def get_data(self) -> dict:
        return self.data

    def get_nonce(self) -> int:
        return self.nonce

    def get_timestamp(self) -> str:
        return self.timestamp

    def __str__(self) -> str:
        return str('\nBlock number: %s\nBlock hash: %s\nPrevious block hash: %s\nBlock data: %s\nBlock nonce: %s\nBlock timestap: %s' % (
            self.number,
            self.hash,
            self.previous_block_hash,
            self.get_data(),
            self.get_nonce(),
            self.get_timestamp()
            ))


class Blockchain:
    DIFFICULTY = 4

    def __init__(self, chain=[]):
        self.chain = chain

    def add_block(self, block):
        self.chain.append(block)

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
