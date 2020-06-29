import requests
import json
import time
import hmac
import hashlib
import base64

from tauros_api import exceptions
from tauros_api.response import Response

api_url = 'https://api.tauros.io'
api_staging_url = 'https://api.staging.tauros.io'


class TaurosAPI():
    """
    This class content a methods series for connection with Tauros API.
    Private requests.
    Multiples methods: get, post, put, patch and delete.
    """

    def __init__(self, api_key, api_secret, staging=False):
        """
        :param api_key: tauros valid api_key
        :type api_key: str

        :param api_secret: tauros valid secret key
        :type api_secret: str
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.api_url = api_url if not staging else api_staging_url

    def _request(self, path, data={}, params={}, method='POST', **extras):
        """
        :param path: destination route sans host
        :type path: str
        :required path: True

        :param data: request body
        :type data: dict
        :required data: False

        :param params: query get &foo=bar
        :type params: dict
        :required params: False

        :param method: request method
        :type method: str
        :required method: False
        :default method: POST

        :param headers: additional request headers
        :type headers: dict
        :required headers: False
        """

        nonce = str(self._nonce())
        signature = self._sign(data, nonce, method, path)

        headers = {
            'Authorization': 'Bearer {}'.format(self.api_key),
            'Taur-Signature': signature,
            'Taur-Nonce': nonce,
            'Content-Type': 'application/json'
        }

        headers.update(extras)

        server_res = requests.request(
            method=method,
            url=self.api_url + path,
            headers=headers,
            params=params,
            data=json.dumps(data),
        )

        response = Response()
        response.status_code = server_res.status_code
        response.body = server_res.json()
        return response

    def _sign(self, data, nonce, method, path):
        """
        :param data: body request data
        :type data: dict
        """
        if not isinstance(data, dict):
            return None
        try:
            request_data = json.dumps(data)

            message = str(nonce) + method.upper() + path + request_data

            api_sha256 = hashlib.sha256(message.encode()).digest()

            api_hmac = hmac.new(base64.b64decode(self.api_secret), api_sha256, hashlib.sha512)

            api_signature = base64.b64encode(api_hmac.digest())

        except Exception:
            raise exceptions.ValidationError('api_secret invalid')

        return api_signature.decode()

    def _nonce(self):
        """
        :returns: an always-increasing unsigned integer (up to 64 bits wide)
        """
        return int(1000*time.time())

    def get(self, path, params={}):
        return self._request(path, params, method='GET')

    def post(self, path, data={}):
        return self._request(path, data, method='POST')

    def put(self, path, data={}):
        return self._request(path, data, method='PUT')

    def patch(self, path, data={}):
        return self._request(path, data, method='PATCH')

    def delete(self, path):
        return self._request(path, method='DELETE')
