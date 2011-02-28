import json
import unittest

import mock

from poundpay.client import Client


class ClientTest(unittest.TestCase):

    @property
    def production_config(self):
        return {
            'developer_sid': 'DV0383d447360511e0bbac00264a09ff3c',
            'auth_token': 'c31155b9f944d7aed204bdb2a253fef13b4fdcc6ae15402004',
        }

    @property
    def sandbox_config(self):
        return {
            'developer_sid': 'DV0383d447360511e0bbac00264a09ff3c',
            'auth_token': 'c31155b9f944d7aed204bdb2a253fef13b4fdcc6ae15402004',
            'api_url': 'https://api-sandbox.poundpay.com',
            'api_version': 'gold',
        }

    def test_developer_sid_and_auth_token_required(self):
        with self.assertRaises(ValueError):
            Client('DV', None)

    def test_developer_sid_starts_with_DV(self):
        config = self.production_config
        with self.assertRaises(ValueError):
            Client(config['auth_token'], config['developer_sid'])

    def test_default_url_and_version(self):
        config = self.production_config
        client = Client(**config)
        self.assertEqual(client.base_url,
                         'https://api.poundpay.com/silver/')
        self.assertIn('Authorization', dict(client.opener.addheaders))
        authstring = dict(client.opener.addheaders)['Authorization'][6:]
        developer_sid, auth_token = authstring.decode('base64').split(':')
        self.assertEqual(developer_sid, config['developer_sid'])
        self.assertEqual(auth_token, config['auth_token'])

    def test_different_url_and_version(self):
        client = Client(**self.sandbox_config)
        self.assertEqual(client.base_url,
                         'https://api-sandbox.poundpay.com/gold/')

    def test_get(self):
        return
        client = Client(**self.production_config)
        resp_dict = {'foo': 'bar'}
        mock_open = mock.mocksignature(client.opener.open)
        mock_open.return_value = json.dumps(resp_dict)
        with mock.patch.object(client.opener, 'open', new=mock_open):
            resp = client.get('payments')
        self.assertEqual(resp.json, resp_dict)
