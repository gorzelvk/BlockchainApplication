# See PyCharm help at https://www.jetbrains.com/help/pycharm/
""" This file contains functions and tools required to create blockchain network"""
import hashlib

def compute_hash(arg):
    hash = hashlib.sha256()
    hash.update(arg.encode('utf-8'))
    return hash.hexdigest()

