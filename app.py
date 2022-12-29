import time
import stripe
import sqltools
from flask import Flask, render_template, flash, redirect, session, request, logging, url_for, jsonify
from passlib.hash import sha256_crypt
from flask_mysqldb import MySQL
from functools import wraps

from blockchaintools import INITIAL_COIN_AMOUNT, PRICE_LIST, INITIAL_PRICE
from sqltools import *
from forms import *

app = Flask(__name__)

# database setup
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'OzzyCoin'
app.config['MYSQL_DB'] = 'OzzyChain'
app.config['MYSQL_CURSOR'] = 'DictCursor'

stripe_keys = {
  'secret_key': 'sk_test_7mJuPfZsBzc3JkrANrFrcDqC',
  'publishable_key': 'pk_test_51AROWSJX9HHJ5bycpEUP9dK39tXufyuWogSUdeweyZEXy3LC7M8yc5d9NlQ96fRCVL0BlAu7Nqt4V7N5xZjJnrkp005fDiTMIr'
}
stripe.api_key = stripe_keys['secret_key']

mysql = MySQL(app)

@app.route('/payment', methods=['GET', 'POST'])
def payment():
    price = request.args['price']
    amount = request.args['amount']
    if request.method == 'POST':
        send_money("bankacc@ozzychain.com", session.get('email'), amount)
        flash(f"You bought {amount} Ozzies!", "success")
        return render_template('charge.html', key=stripe_keys['publishable_key'], amount=amount)
    return render_template('payment.html', key=stripe_keys['publishable_key'], price=float(price)*float(amount))
@app.route('/charge', methods=['GET', 'POST'])
def charge():
    return render_template('charge.html')

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
        wallet_address = sha256_crypt.encrypt(email)
        if sqltools.check_user_exist(email):
            password = sha256_crypt.encrypt(form.password.data)
            users.insert_values(name, email, password, wallet_address)
            log_in_user(email)
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
        user = users.get_single_value("email", email)
        actual_password = None
        try:
            actual_password = user[2]
        except Exception:
            pass
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


@app.route("/transaction", methods=['GET', 'POST'])
@is_logged_in
def transaction():
    form = SendMoneyForm(request.form)
    balance = check_balance(session.get('email'))

    if request.method == 'POST':
        try:
            send_money(session.get('email'), form.email.data, form.amount.data)
            flash("Ozzies sent!", "success")
        except Exception as e:
            flash(str(e), "danger")

        return redirect(url_for('transaction'))
    return render_template('transaction.html', balance=balance, form=form, page='transaction')


@app.route("/buy", methods=['GET', 'POST'])
@is_logged_in
def buy():
    price_list = []
    timestamps_list = []
    ozzy_price_sql = Table("ozzyprice", "price", "timestamp")
    ozzy_price = ozzy_price_sql.get_all_values()
    for i in range(len(ozzy_price)):
        price_list.append(float(ozzy_price[i][0]))
        timestamps_list.append(ozzy_price[i][1])

    form = BuyForm(request.form)
    print(form.amount.data)
    balance = check_balance(session.get('email'))
    if request.method == 'POST':
        try:
            price = price_list[-1] * 100
            return redirect(url_for('payment', price=price, amount=form.amount.data))
        except Exception as e:
            flash(str(e), "danger")
        return redirect(url_for('buy'))
    return render_template('buy.html', balance=balance, form=form, page='buy', key=stripe_keys['publishable_key'])


@app.route("/sell", methods=['GET', 'POST'])
@is_logged_in
def sell():
    form = BuyForm(request.form)
    balance = check_balance(session.get('email'))
    if request.method == 'POST':
        try:
            send_money(session.get('email'), "bankacc@ozzychain.com", form.amount.data)
            flash(f"You sold {form.amount.data} Ozzies!", "success")
        except Exception as e:
            flash(str(e), "danger")
        return redirect(url_for('sell'))
    return render_template('sell.html', balance=balance, form=form, page='sell')

@app.route("/logout")
@is_logged_in
def logout():
    session.clear()
    flash("Logout success", 'success')
    return redirect(url_for('login'))


@app.route("/dashboard")
@is_logged_in
def dashboard():
    price_list = []
    timestamps_list = []
    ozzy_price_sql = Table("ozzyprice", "price", "timestamp")
    ozzy_price = ozzy_price_sql.get_all_values()
    for i in range(len(ozzy_price)):
        price_list.append(round(float(ozzy_price[i][0]), 3))
        timestamps_list.append(ozzy_price[i][1])

    print(price_list)
    print(timestamps_list)
    blockchain = get_blockchain().chain
    timenow = time.strftime("%I:%M %p")
    return render_template('dashboard.html', session=session, timenow=timenow, blockchain=blockchain, page='dashboard', ozzy_price=price_list, timestamps=timestamps_list)


@app.route("/")
def landing_page():
    return render_template('landing_page.html')


if __name__ == "__main__":
    # secret key is used to prevent cookie tampering
    app.secret_key = 'b547dd6982e53290703af3da6d4fb016647f2edbb169897987c16b9bf2c81f38'
    app.run(debug=True)

