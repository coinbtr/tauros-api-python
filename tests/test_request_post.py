# Standard library imports...
from unittest import TestCase
try:
    from unittest.mock import patch, MagicMock
except ImportError:
    from mock import patch, MagicMock

from tauros_api.request import TaurosAPI

class Response():
    body = None
    def json(self):
        return self.body


class RequestPost(TestCase):
    api_key = 'cae5fb9186b7f940d2a9031e79f0d58043ebf114'
    api_secret = 'eada71676b6a9c1189f120160288bfed6610c87ea352a7c61ae6406ac64bb58f'

    def setUp(self):
        self.tauros = TaurosAPI(api_key=self.api_key, api_secret=self.api_secret)

    @patch('time.time', MagicMock(return_value=12345))
    def test_sign_method(self):
        _signature = '8g863L/B/cfzMePFMe6CsY4c3Hp7uZx+7gN6qOuR/qOiTtgx927w6FpPPA8bp+4e7Dja2a/NN78LFLQvCuXRrg=='
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
            'number': '23872674',
            'phone_number': '+52*******330',
            'phone_verified': False,
            'pk': 1,
            'preference': {'coin_symbol': '\u20ac', 'default_coin': 'MXN'},
            'reference_link': 'bW9pc2VzQHThdXdvcy5pbw==',
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
