import time
import ccxt
from flask import Flask, render_template, Response, stream_with_context, jsonify


app = Flask(__name__)
global binance, btc, trx, caldot
binance = ccxt.binance()

def cal_DOT(total, col):
    global btc
    return (total-col[3]-col[2]-col[1]*btc)/col[0]

def get_tdr():
    global btc, trx, caldot
    try:
        with open('tdr.txt', 'r', encoding='utf-8') as tdr_file:
            lines = tdr_file.readlines()
            total = int(lines[0])
            collateral = [float(col) for col in lines[1].split()]
            print(total)
            print(collateral)
            caldot = cal_DOT(total, collateral)
            print(caldot)
            return caldot
    except:
        return caldot
    

def get_prices():
    global binance, btc, trx
    btc = binance.fetch_ticker('BTC/BUSD')['close']
    trx = binance.fetch_ticker('TRX/BUSD')['close']
    return btc, trx

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/update', methods=['POST'])
def update():
    btc, trx = get_prices()
    btc_price = 'BTC/BUSD : {}'.format(btc)
    trx_price = 'TRX/BUSD(present) : {}'.format(trx)
    trx_dot = get_tdr()
    return jsonify({
        'btc_busd': btc_price,
        'trx_busd' : trx_price,
        'trx_dot': 'TRX/BUSD(BOOM!) : {}'.format(trx_dot),
    })



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=12356)
