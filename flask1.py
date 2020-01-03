from flask import Flask, request, render_template
import datetime 
import json 
import hashlib
import os
from logging.handlers import RotatingFileHandler
import logging
import requests
from requests.exceptions import HTTPError
from config import SHOP_ID,SHOP_SECRET_KEY

app = Flask(__name__)
app.config.from_object('config')
app.debug = False
port = int(os.environ.get('PORT', 5000))
app.run()

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'SecretKey01'

def css_styles(name, charset='utf-8'):
    with app.open_resource(name) as f:
        return f.read().decode(charset)

app.jinja_env.globals['css_styles'] = css_styles
payment_id = 0
shop_id=5

def generate_sign(prm):
    text = ''
    for key in sorted(prm):
        if text:
            text += ':'
        text += str(prm[key])

    return hashlib.md5(text.encode('utf-8')).hexdigest()

def init_log_handler():
    logHandler = RotatingFileHandler('log.log')
    handler = logging.StreamHandler()
    handler.setLevel(logging.ERROR)
    app.logger.addHandler(handler)

def logs(currency, amount, datetime, description, payment_id):    
    app.logger.info(
        json.dumps(str({'currency': currency, 'amount': amount, 'datetime': datetime, 
            'description': description, 'payment_id': payment_id})))

@app.route('/')
@app.route('/index')
def index():
    init_log_handler()
    return render_template('index.html')

def eur(amount, currency, shop_id, shop_order_id, methods=['GET, POST']):
#по протоколу Pay
    currency = 978
    shop_order_id = '123456'
    sign = generate_sign({'amount': amount, 'currency': currency, 'shop_id': shop_id, 'shop_order_id': shop_order_id})

for url in ['/pay.piastrix.com/en/pay']:
    try:
        response = requests.get(url)
        if r.status_code == requests.codes.ok:
            logs(currency, amount, str(datetime.datetime.now()), description, payment_id)
        # если ответ успешен, исключения задействованы не будут
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'Ошибка оплаты')
    except Exception as err:
        print(f'Ошибка оплаты') 
    else:
        print('Оплата произведена!')

def usd(shop_amount, shop_currency, shop_id, shop_order_id, payer_currency):
#метод Bill
    payer_currency = 840
    shop_order_id = '123456'
    sign = generate_sign({'shop_amount': shop_amount, 'shop_currency': shop_currency, 'shop_id': shop_id, 'shop_order_id': shop_order_id, 'payer_currency': payer_currency})

for url in ['/​https://core.piastrix.com/bill/create']:
    try:
        response = requests.get(url)
        if r.status_code == requests.codes.ok:
            logs(currency, amount, str(datetime.datetime.now()), description, payment_id)
        # если ответ успешен, исключения задействованы не будут
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'Ошибка оплаты')
    except Exception as err:
        print(f'Ошибка оплаты')
    else:
        print('Оплата произведена!')




def rub(amount, payer_currency, payway, shop_id, shop_order_id, sign):
#метод Invoice
    currency = 643
    payway = 'payeer_rub'
    shop_order_id = '123456'
    sign = generate_sign({'amount': amount, 'currency': currency, 'payway': payway, 'shop_id': shop_id, 'shop_order_id': shop_order_id, 'sign': sign })

for url in ['/​https://core.piastrix.com/invoice/create']:
    try:
        response = requests.get(url)
        if r.status_code == requests.codes.ok:
            logs(currency, amount, str(datetime.datetime.now()), description, payment_id)
        # если ответ успешен, исключения задействованы не будут
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'Ошибка оплаты')
    except Exception as err:
        print(f'Ошибка оплаты')
    else:
        print('Оплата произведена!')


@app.route('/pay', methods=['GET', 'POST'])
def pay():
    shop_order_id = '123456'

    if request.method == 'POST':
        amount  = request.form.get('amount', None)
        currency  = request.form.get('currency', None)
        description  = request.form.get('description', None)

        if not amount:
            return 'Вы не ввели сумму оплаты'

        global payment_id
        payment_id += 1


