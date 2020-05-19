# Tauros API V2 Python Module.

## How To Install
```sh
$ pip install tauros-api
```

## How To Use
```py
from tauros_api import TaurosAPI

tauros = TaurosAPI(
  api_key='<token>',
  api_secret='<secret-key>'
)

path = '/api/v2/example/'

data = {
  'key1': 'value',
  'key2': 'value'
}

response = tauros.post(path, data)

print(response.status_code) # 200

print(response.body.success) # True
print(response.body.code) # 0000
print(response.body.msg) # some message
print(response.body.payload) # { ... }
```
