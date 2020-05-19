import requests
import json
import time
import hmac
import hashlib
import base64
import urllib.parse


class TaurosAPI():
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret

    def _request(self, path, data, signature):
        pass

    def _sign(self, data):
        request_data = urllib.parse.urlencode(data)

        api_sha256 = hashlib.sha256(request_data.encode()).digest()

        api_hmac = hmac.new(base64.b64decode(self.api_secret), api_sha256, hashlib.sha512)

        api_signature = base64.b64encode(api_hmac.digest())

        return sigdigest.decode()

    def post(self, path, data={}):
        pass

    def get(self, path, params={}):
        pass
