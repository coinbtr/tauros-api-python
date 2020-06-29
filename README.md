# Tauros API V2 Python Module.

[![Build Status](https://travis-ci.org/coinbtr/tauros-api-python.svg?branch=master)](https://travis-ci.org/coinbtr/tauros-api-python)
[![Coverage Status](https://coveralls.io/repos/github/coinbtr/tauros-api-python/badge.svg?branch=master)](https://coveralls.io/github/coinbtr/tauros-api-python?branch=master)

## How To Install
```sh
$ pip install tauros-api
```

## How To Use
```py
from tauros_api import TaurosAPI

api_key = '5b4c752447da0494ddbaeb4a8e046550fd43f21a'

api_secret = 'ZjhiNGVhOTNlZDZkNTJlOTE5MzlhNjFjNWQwNjI2MjFhZjM4N2I5YTE4OTYyMWQ0MjU2MTliNDk3ZjYxODE1Mg=='

tauros = TaurosAPI(api_key, api_secret, staging=True) # default staging=False

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
