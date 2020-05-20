import requests
import json
import time
import hmac
import hashlib
import base64
import urllib.parse

from tauros_api import exceptions

URIs = {
    'production': 'https://api.tauros.io',
    'staging': 'https://api.staging.tauros.io',
    'local': 'http://localhost:8000' # borrar antes de subir cambio
}


class Response:
    """
    Tauros API Object response.
    """
    pass


class TaurosAPI():
    """
    This class content a methods series for connection with Tauros API.
    Private requests.
    Multiples methods: get, post, put, patch and delete.
    """

    def __init__(self, api_key, api_secret, environment='production'):
        """
        :param api_key: tauros valid api_key
        :type api_key: str

        :param api_secret: tauros valid secret key
        :type api_secret: str

        :param environment: API environment ('production', staging) by default is 'production'
        :type environment: str
        """
        if not environment in ['production', 'staging', 'local']: # delete local option antes de publicar
            raise exceptions.ValidationError("environment field is not valid")

        self.url_api = URIs.get(environment)
        self.api_key = api_key
        self.api_secret = api_secret
        self.headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'Authorization': 'Bearer {}'.format(self.api_key)
        }
        return

    def _request(self, path, data={}, params={}, method='POST', headers={}):
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

        headers = {
            **self.headers,
            **headers
        }

        server_res = requests.request(
            method=method,
            url=self.url_api + path,
            headers=headers,
            params=params,
            data=json.dumps(data),
        )

        response = Response()
        response.status_code = server_res.status_code
        response.body = server_res.json()
        return response

    def _sign(self, data):
        """
        :param data: body request data
        :type data: dict
        """
        request_data = urllib.parse.urlencode(data)

        api_sha256 = hashlib.sha256(request_data.encode()).digest()

        api_hmac = hmac.new(base64.b64decode(self.api_secret), api_sha256, hashlib.sha512)

        api_signature = base64.b64encode(api_hmac.digest())

        return api_signature.decode()

    def _nonce(self):
        """
        :returns: an always-increasing unsigned integer (up to 64 bits wide)
        """
        return int(1000*time.time())


    def _signed_request(self, path, data):
        """
        :param path: destination route sans host
        :type path: str

        :param data: request body
        :type data: dict

        :returns: response data
        """
        # set nonce field to request body
        data['nonce'] = self._nonce()
        signature = self._sign(data)
        headers = {
            'Taur-Signature': signature
        }

        response = self._request(path, data=data, headers=headers)

        return response

    def post(self, path, data={}):
        return self._signed_request(path, data)

    def get(self, path, params={}):
        return self._request(path, params, method='GET')

    def put(self, path, data={}):
        return self._request(path, method='PUT')

    def patch(self, path, data={}):
        return self._request(path, method='PATCH')

    def delete(self, path):
        return self._request(path, method='DELETE')
