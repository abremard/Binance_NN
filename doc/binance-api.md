# Binance API
## Setup
Install lib:
```
pip install python-binance
```
Store creds as env var:
```
set binance_api=your_api_key_here
set binance_secret=your_api_secret_here
```
```
API Key: g852Dn6vv1zQ3zFJ6s9KCilduMTC3EZXbqgPUywhotpnBWK7ZPtd0LmDv4e5COVF
Secret Key: CuaRMQpu8UqKNyyqS1F7hDRz5hXUqaesOEH4pnRhlfG3Ql3rTbzX4PsiBqxhZ122
```
## Account Balance
```
import os
from binance.client import Client

# init
api_key = os.environ.get('binance_api')
api_secret = os.environ.get('binance_secret')

client = Client(api_key, api_secret)

client.API_URL = 'https://testnet.binance.vision/api'

# get balances for all assets & some account information
print(client.get_account())

# get balance for a specific asset only (BTC)
print(client.get_asset_balance(asset='BTC'))
```

## Latest Price

```
# get latest price from Binance API
btc_price = client.get_symbol_ticker(symbol="BTCUSDT")
# print full output (dictionary)
print(btc_price) # print(btc_price["price"])
```

## Web Socket

```
import os

from binance.client import Client
from binance.websockets import BinanceSocketManager
from twisted.internet import reactor

def btc_trade_history(msg):
    ''' define how to process incoming WebSocket messages '''
    if msg['e'] != 'error':
        print(msg['c'])
        btc_price['last'] = msg['c']
        btc_price['bid'] = msg['b']
        btc_price['last'] = msg['a']
    else:
        btc_price['error'] = True

# init and start the WebSocket
bsm = BinanceSocketManager(client)
conn_key = bsm.start_symbol_ticker_socket('BTCUSDT', btc_trade_history)
bsm.start()

# stop websocket
bsm.stop_socket(conn_key)

# properly terminate WebSocket
reactor.stop()

```

## Historical Data

```
# valid intervals - 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M

# get timestamp of earliest date data is available
timestamp = client._get_earliest_valid_timestamp('BTCUSDT', '1d')
print(timestamp)

# request historical candle (or klines) data
bars = client.get_historical_klines('BTCUSDT', '1d', timestamp, limit=1000)

# option 1 - save to file using json method
with open('btc_bars.json', 'w') as e:
    json.dump(bars, e)

# option 2 - create a Pandas DataFrame and export to CSV
# delete unwanted data - just keep date, open, high, low, close
for line in bars:
    del line[5:]
btc_df = pd.DataFrame(bars, columns=['date', 'open', 'high', 'low', 'close'])
btc_df.set_index('date', inplace=True)
print(btc_df.head())
# export DataFrame to csv
btc_df.to_csv('btc_bars.csv')

```

## Technical Indicators

```
import btalib
import pandas as pd

# load DataFrame
btc_df = pd.read_csv('btc_bars.csv', index_col=0)
#btc_df.set_index('date', inplace=True)
btc_df.index = pd.to_datetime(btc_df.index, unit='ms')

# create sma and attach as column to original df
btc_df['sma'] = btalib.sma(btc_df.close, period=20).df
print(btc_df.tail())

```

## Fire Order

```

buy_order_limit = client.create_test_order(
    symbol='ETHUSDT',
    side='BUY',
    type='LIMIT',
    timeInForce='GTC',
    quantity=100,
    price=200)

buy_order = client.create_test_order(symbol='ETHUSDT', side='BUY', type='MARKET', quantity=100)

# cancel previous orders
cancel = client.cancel_order(symbol='ETHUSDT', orderId=buy_limit['orderId'])

```

## Stoploss Takeprofit

```

try:
    order = client.create_oco_order(
        symbol='ETHUSDT',
        side='SELL',
        quantity=100,
        price=250,
        stopPrice=150,
        stopLimitPrice=150,
        stopLimitTimeInForce='GTC')

except BinanceAPIException as e:
    # error handling goes here
    print(e)
except BinanceOrderException as e:
    # error handling goes here
    print(e)

```

## Discounted Commission

```

def topup_bnb(min_balance: float, topup: float):
	''' Top up BNB balance if it drops below minimum specified balance '''
	bnb_balance = client.get_asset_balance(asset='BNB')
	bnb_balance = float(bnb_balance['free'])
	if bnb_balance < min_balance:
		qty = round(topup - bnb_balance, 5)
		print(qty)
		order = client.order_market_buy(symbol='BNBUSDT', quantity=qty)
		return order
	return False

min_balance = 1.0
topup = 2.5
order = topup_bnb(min_balance, topup)

```