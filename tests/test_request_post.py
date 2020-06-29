# Standard library imports...
from unittest import TestCase
try:
    from unittest.mock import patch, MagicMock
except ImportError:
    from mock import patch, MagicMock

from tauros_api.request import TaurosAPI
from tauros_api import exceptions

class Response():
    body = None
    def json(self):
        return self.body


class RequestSuccess(TestCase):
    api_key = '5b4c752447da0494ddbaeb4a8e046550fd43f21a'
    api_secret = 'ZjhiNGVhOTNlZDZkNTJlOTE5MzlhNjFjNWQwNjI2MjFhZjM4N2I5YTE4OTYyMWQ0MjU2MTliNDk3ZjYxODE1Mg=='

    def setUp(self):
        self.tauros = TaurosAPI(api_key=self.api_key, api_secret=self.api_secret)

    @patch('time.time', MagicMock(return_value=12345))
    def test_sign_method(self):
        _signature = '1Vs8kXcd6xTW7LigOJeyhYdrIqVYuHmg/Z6jWG/0qZinv6cGZlkjLOfan657CEI+Tr8cJW/nV1SrcKA+NTDkvQ=='
        nonce = self.tauros._nonce()
        method = 'POST'
        path = '/api/v2/test/'
        data = {
            'age': 23,
            'email': 'moisesdelacruz.dev@gmail.com',
            'name': 'Moises De La Cruz'
        }
        signature = self.tauros._sign(data, nonce, method, path)
        self.assertEqual(_signature, signature)

    @patch('requests.request')
    def test_post_response_is_ok(self, mock_get):
        # simulate response
        exam_body = {
            'side': 'buy',
            'market': 'BTC-MXN',
            'amount': '0.01',
            'price': '100000',
            'type': 'limit',
            'is_amount_value': True
        }

        exam_res = Response()
        exam_res.status_code = 200

        mock_get.return_value = exam_res

        # Call the service, which will send a request to the server.
        path = '/api/v1/trading/placeorder/'

        data = {
            "market": "BTC-MXN",
            "amount": "0.001",
            "side": "SELL",
            "type": "LIMIT",
            "price": "250000"
        }
        response = self.tauros.post(path, data)

        # If the request is sent successfully, then I expect a response to be returned.
        self.assertEqual(response.status_code, 200)


    @patch('requests.request')
    def test_get_method(self, mock_get):
        # simulate response
        exam_body = {
            'biometric_verified': False,
            'birthdate': '1996-09-06',
            'can_request_card': False,
            'email': 'Foo@tauros.io',
            'first_name': 'Foo',
            'has_cacao_kyc': False,
            'has_kyc': True,
            'has_nip': True,
            'has_signature': False,
            'is_active': True,
            'is_developer': True,
            'is_referred': False,
            'is_staff': True,
            'is_superuser': True,
            'last_name': 'Bar',
            'level': 1,
            'number': '23812674',
            'phone_number': '+52*******330',
            'phone_verified': False,
            'pk': 1,
            'preference': {'coin_symbol': '\u20ac', 'default_coin': 'MXN'},
            'reference_link': 'bW9pc2VzQHEhdXdvcy5pbw==',
            'require_password_change': False,
            'second_last_name': '1',
            'two_factor': False,
            'verification_in_process': False
        }

        exam_res = Response()
        exam_res.status_code = 200
        exam_res.body = exam_body

        mock_get.return_value = exam_res

        path = '/api/v1/perofile/'

        response = self.tauros.get(path)

        # If the request is sent successfully, then I expect a response to be returned.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.body, exam_body)

    @patch('requests.request')
    def test_patch_method(self, mock_patch):
        exam_body = {
            'phone_number': '+525523236412',
        }
        exam_res = Response()
        exam_res.status_code = 200
        exam_res.body = exam_body

        mock_patch.return_value = exam_res

        path = '/api/v1/perofile/'

        response = self.tauros.patch(path, exam_body)

        # If the request is sent successfully, then I expect a response to be returned.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.body, exam_body)

    @patch('requests.request')
    def test_put_method(self, mock_put):
        exam_body = {
            'name': 'foo',
            'last': 'bar'
        }
        exam_res = Response()
        exam_res.status_code = 200
        exam_res.body = exam_body

        mock_put.return_value = exam_res

        path = '/api/v1/test/'

        response = self.tauros.put(path, exam_body)
        self.assertEqual(response.body, exam_body)

        # If the request is sent successfully, then I expect a response to be returned.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.body, exam_body)

    @patch('requests.request')
    def test_delete_method(self, mock_delete):
        exam_res = Response()
        exam_res.status_code = 204

        mock_delete.return_value = exam_res

        path = '/api/v1/perofile/'

        response = self.tauros.delete(path)

        # If the request is sent successfully, then I expect a response to be returned.
        self.assertEqual(response.status_code, 204)


class BadRequest(TestCase):
    api_key = '5b4c752447da0494ddbaeb4a8e046550fd43f21a'
    api_secret = 'hello tauros'

    def setUp(self):
        self.tauros = TaurosAPI(api_key=self.api_key, api_secret=self.api_secret)

    @patch('time.time', MagicMock(return_value=12345))
    def test_sign_method_invalid_data(self):
        nonce = self.tauros._nonce()
        method = 'POST'
        path = '/api/v2/test/'
        data = 12
        signature = self.tauros._sign(data, nonce, method, path)
        self.assertEqual(None, signature)

    @patch('time.time', MagicMock(return_value=12345))
    def test_sign_method_bad_api_secret(self):
        nonce = self.tauros._nonce()
        method = 'POST'
        path = '/api/v2/test/'
        data = {}
        with self.assertRaises(exceptions.ValidationError) as context:
            self.tauros._sign(data, nonce, method, path)
        self.assertEqual('api_secret invalid', str(context.exception))
