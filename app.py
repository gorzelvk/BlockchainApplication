import hashlib

import blockchaintools
from flask import Flask, render_template, flash, redirect, session, request, logging
from passlib.hash import sha256_crypt
from flask_mysqldb import MySQL
from sqltools import *

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'OzzyCoin'
app.config['MYSQL_DB'] = 'OzzyChain'
app.config['MYSQL_CURSOR'] = 'DictCursor'

mysql = MySQL(app)


@app.route("/")
def landing_page():
    users = Table("users", "name", "wallet_address", "email", "password")
    users.insert_values("test", hashlib.sha256().update("wallet".encode('utf-8')), "email", "password")
    users.drop_table()
    return render_template('landing_page.html')


if __name__ == "__main__":
    blockchain = blockchaintools.Blockchain()
    database = [
        "amount 3", "amount 2", "amount 8", "amount 30", "amount 40"
        ]

    for data in database:
        blockchain.mine_block(blockchaintools.Block(data))

    app.run(debug=True)
    app.secret_key = 'b547dd6982e53290703af3da6d4fb016647f2edbb169897987c16b9bf2c81f38'
