# Tauros API V2 Python Module.

[![Build Status](https://travis-ci.org/coinbtr/tauros-api-python.svg?branch=master)](https://travis-ci.org/coinbtr/tauros-api-python)

## How To Install
```sh
$ pip install tauros-api
```

## How To Use
```py
from tauros_api import TaurosAPI

api_key = 'cae5fb9186b7f940d2a9031e79f0d58043ebf114'

api_secret = 'eada71676b6a9c1189f120160288bfed6610c87ea352a7c61ae6406ac64bb58f'

tauros = TaurosAPI(api_key, api_secret)

path = '/api/v1/trading/placeorder/'

data = {
    "market": "BTC-MXN",
    "amount": "0.001",
    "side": "SELL",
    "type": "LIMIT",
    "price": "250000"
}

response = tauros.post(path, data)

print(response.status_code) # 200

print(response.body['success']) # True
print(response.body['code']) # 0000
print(response.body['msg']) # some message
print(response.body['payload']) # { ... }
```
