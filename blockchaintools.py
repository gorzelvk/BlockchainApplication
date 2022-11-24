""" This file contains functions and tools required to create blockchain network """
import hashlib
from typing import Optional
from datetime import datetime

GENESIS_HASH = 0


def compute_hash(*args) -> str:
    hashed_element = ''
    hash_result = hashlib.sha256()

    # hash each argument
    for arg in args:
        hashed_element += str(arg)

    hash_result.update(hashed_element.encode('utf-8'))
    return hash_result.hexdigest()


class Block:
    """ Block is a basic container of information in blockchain """
    number: int
    previous_block_hash: Optional['Block']
    data: Optional[dict]
    nonce: int

    def __init__(self, previous_block_hash=None, data=None, nonce=0):
        if previous_block_hash is None:
            self.number = 0
        else:
            self.number = 1  # TODO

        self.previous_block_hash = previous_block_hash
        self.data = data
        self.nonce = nonce
        self.timestamp = datetime.now()

    def get_previous_hash(self):
        if self.previous_block_hash is None:
            return GENESIS_HASH
        else:
            return self.previous_block_hash.get_hash()

    def get_hash(self) -> str:
        return compute_hash(self.get_previous_hash(), self.data, self.nonce, self.timestamp)

    def mine(self, difficulty: int) -> None:
        while self.get_hash()[:difficulty] != '0' * difficulty:
            self.nonce += 1

    def get_data(self) -> dict:
        return self.data

    def get_nonce(self) -> int:
        return self.nonce

    def get_timestamp(self) -> str:
        return self.timestamp

    def __str__(self) -> str:
        return str('\nBlock number: %s\nBlock hash: %s\nPrevious block hash: %s\nBlock data: %s\nBlock nonce: %s\nBlock timestap: %s' % (
            self.number,
            self.get_hash(),
            self.get_previous_hash(),
            self.get_data(),
            self.get_nonce(),
            self.get_timestamp()
            ))


