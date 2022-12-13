import hashlib

import blockchaintools
from flask import Flask, render_template, flash, redirect, session, request, logging, url_for
from passlib.hash import sha256_crypt
from flask_mysqldb import MySQL
from functools import wraps

import sqltools
from sqltools import *
from forms import *

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'OzzyCoin'
app.config['MYSQL_DB'] = 'OzzyChain'
app.config['MYSQL_CURSOR'] = 'DictCursor'


mysql = MySQL(app)


def log_in_user(email):
    users = Table("users", "name", "email", "password", "wallet_address")
    user = users.get_single_value("email", email)

    session['logged_in'] = True
    session['email'] = email
    session['name'] = user[0]


def is_logged_in(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return func(*args, **kwargs)
        else:
            flash("You have no access to this page, please login", "danger")
            return redirect(url_for('login'))
    return wrap


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    users = Table("users", "name", "email", "password", "wallet_address")
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        wallet_address = "kacper_address"
        if sqltools.check_user_exist(name):
            password = sha256_crypt.encrypt(form.password.data)
            users.insert_values(name, email, password, wallet_address)
            log_in_user(name)
            return redirect(url_for('dashboard'))
        else:
            flash('User already exists', 'danger')
            return redirect(url_for('register'))

    return render_template('register.html', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password_provided = request.form['password']

        users = Table("users", "name", "email", "password", "wallet_address")
        user = users.get_single_value("email", email)  # (Name, Email, Password, Wallet_Address)
        actual_password = None
        if 2 in user:
            actual_password = user[2]
        print(actual_password)

        if actual_password is None:
            flash('User not found', 'danger')
            return redirect(url_for('login'))
        else:
            if sha256_crypt.verify(password_provided, actual_password):
                log_in_user(email)
                flash('You are logged in!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Wrong Password', 'danger')
                return redirect(url_for('login'))

    return render_template('login.html')


@app.route("/logout")
@is_logged_in
def logout():
    session.clear()
    flash("Logout success", 'success')
    return redirect(url_for('login'))


@app.route("/dashboard")
@is_logged_in
def dashboard():
    return render_template('dashboard.html', session=session)

@app.route("/")
def landing_page():
    # users.insert_values("test", hashlib.sha256().update("wallet".encode('utf-8')), "email", "password")
    # users.drop_table()
    return render_template('landing_page.html')


if __name__ == "__main__":
    blockchain = blockchaintools.Blockchain()
    database = [
        "amount 3", "amount 2", "amount 8", "amount 30", "amount 40"
        ]

    for data in database:
        blockchain.mine_block(blockchaintools.Block(data))

    app.secret_key = 'b547dd6982e53290703af3da6d4fb016647f2edbb169897987c16b9bf2c81f38'
    app.run(debug=True)

