import itertools
from datetime import datetime

import blockchaintools
from app import mysql, session
from blockchaintools import Block, Blockchain


# Exception class for invalid transaction
class InvalidTransactionException(Exception):
    pass


# Exception class for insufficient funds on user's account
class InsufficientFundsException(Exception):
    pass


class Table:
    # EXAMPLE initialization: ...Table("blockchain", "number", "hash", "previous", "data", "nonce", "timestamp")
    def __init__(self, table_name, *args):
        self.table = table_name
        self.columns = "(%s)" % ",".join(args)
        self.columnsList = args

        # if table does not already exist, create it.
        if check_table_exist(table_name):
            create_data = ""
            for column in self.columnsList:
                create_data += "%s varchar(100)," % column

            cursor = mysql.connection.cursor()  # create the table
            cursor.execute("CREATE TABLE %s(%s)" % (self.table, create_data[:len(create_data) - 1]))
            cursor.close()

    # retrieve all values from table
    def get_all_values(self):
        cursor = mysql.connection.cursor()
        result = cursor.execute("SELECT * FROM %s" % self.table)
        data = cursor.fetchall()
        return data

    # retrieve single value from table based on a column's data
    def get_single_value(self, search, value):
        data = {}
        cursor = mysql.connection.cursor()
        result = cursor.execute("SELECT * FROM %s WHERE %s = \"%s\"" % (self.table, search, value))
        if result > 0:
            data = cursor.fetchone()
        cursor.close()
        return data

    # delete single value from table
    def delete(self, search, value):
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE from %s where %s = \"%s\"" % (self.table, search, value))
        mysql.connection.commit()
        cursor.close()

    # function to delete all values from table
    def delete_all_values(self):
        self.drop_table()  # remove table
        self.__init__(self.table, *self.columnsList)  # recreate table

    # function to remove table
    def drop_table(self):
        cursor = mysql.connection.cursor()
        cursor.execute("DROP TABLE %s" % self.table)
        cursor.close()

    # insert values into the table
    def insert_values(self, *args):
        data = ""
        for arg in args:  # convert data into string mysql format
            data += "\"%s\"," % arg

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO %s%s VALUES(%s)" % (self.table, self.columns, data[:len(data) - 1]))
        mysql.connection.commit()
        cursor.close()


# execute mysql code from python
def sql_raw(execution):
    cursor = mysql.connection.cursor()
    cursor.execute(execution)
    mysql.connection.commit()
    cursor.close()


# check if table already exists
def check_table_exist(table_name):
    cursor = mysql.connection.cursor()

    try:  # attempt to get data from table
        result = cursor.execute("SELECT * from %s" % table_name)
        cursor.close()
    except:
        return True
    else:
        return False


# check if user already exists
def check_user_exist(email):
    # access the users table and get all values from column "username"
    users = Table("users", "name", "wallet_address", "email", "password")
    data = users.get_all_values()
    usernames = [user[1] for user in data]
    return False if email in usernames else True


# send money from one user to another
def send_money(sender, recipient, amount):
    # verify that the amount is an integer or floating value
    try:
        amount = float(amount)
    except ValueError:
        raise InvalidTransactionException("Invalid Transaction.")

    # verify that the user has enough money to send (exception if it is the BANK)
    if amount > check_balance(sender) and sender != "bankacc@ozzychain.com":
        raise InsufficientFundsException("Insufficient Funds.")

    # verify that the user is not sending money to themselves or amount is less than or 0
    elif sender == recipient or amount <= 0.00:
        raise InvalidTransactionException("Invalid Transaction.")

    # verify that the recipient exists
    elif check_user_exist(recipient):
        raise InvalidTransactionException("User Does Not Exist.")

    # update the blockchain and sync to mysql
    blockchain = get_blockchain()
    number = len(blockchain.chain) + 1
    data = "%s-->%s-->%s" %(sender, recipient, amount)
    blockchain.mine_block(blockchaintools.Block(number=number, data=data, timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    sync_blockchain(blockchain)
    calculate_ozzy_price()


def calculate_ozzy_price():
    ozzy_price_sql = Table("ozzyprice", "price")
    bank_balance = check_balance('bankacc@ozzychain.com')
    multiplier = (blockchaintools.INITIAL_COIN_AMOUNT - bank_balance) / 100000 + 1
    price = blockchaintools.INITIAL_PRICE * multiplier
    blockchaintools.PRICE_LIST.append(price)
    ozzy_price_sql.insert_values(price)
    return blockchaintools.PRICE_LIST


# check user's account balance
def check_balance(email):
    if email == 'bankacc@ozzychain.com':
        initial_balance = blockchaintools.INITIAL_COIN_AMOUNT
    else:
        initial_balance = 0.0
    blockchain = get_blockchain()

    # loop through the blockchain and update balance
    for block in blockchain.chain:
        data = block.data
        data = data.split('-->')
        if email == data[0]:
            initial_balance -= float(data[2])
        elif email == data[1]:
            initial_balance += float(data[2])
    return initial_balance


# get the blockchain from mysql and convert to Blockchain object
def get_blockchain():
    blockchain = Blockchain()
    blockchain_sql = Table("blockchain", "number", "hash", "previous", "data", "nonce", "timestamp")
    for b in blockchain_sql.get_all_values():
        blockchain.add_block(Block(number=int(b[0]), previous_block_hash=b[2], data=b[3], nonce=int(b[4]), timestamp=b[5]))
    return blockchain


# update blockchain in mysql table
def sync_blockchain(blockchain):
    blockchain_sql = Table("blockchain", "number", "hash", "previous", "data", "nonce", "timestamp")
    blockchain_sql.delete_all_values()
    for b in blockchain.chain:
        blockchain_sql.insert_values(str(b.number), b.get_hash(), b.previous_block_hash, b.data, b.nonce, b.timestamp)
