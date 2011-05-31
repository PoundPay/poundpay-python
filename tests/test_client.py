import os
import json
import unittest

import mock

from poundpay.client import Client, ClientResponse, _url_encode


class TestClientResponse(unittest.TestCase):

    def test_client_response_constructor_arguments(self):
        sentinal_1 = object()
        sentinal_2 = object()
        client_response = ClientResponse(sentinal_1, sentinal_2)
        self.assertIs(client_response.response, sentinal_1)
        self.assertIs(client_response.data, sentinal_2)

    def test_client_json_property(self):
        client_response = ClientResponse(None, json.dumps({'foo': 'bar'}))
        self.assertEqual(client_response.json, {'foo': 'bar'})


class TestClient(unittest.TestCase):

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

    def test_default_api_version_when_explicity_set_to_None(self):
        config = self.production_config
        config['api_version'] = None
        client = Client(**config)
        self.assertTrue(client.base_url.endswith(Client.API_VERSION + '/'))

    def test_default_api_url_when_explicity_set_to_None(self):
        config = self.production_config
        config['api_url'] = None
        client = Client(**config)
        self.assertTrue(client.base_url,
                        os.path.join(client.API_URL, client.API_VERSION))

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
        client = Client(**self.production_config)
        resp_dict = {'foo': 'bar'}
        mock_open = mock.Mock()
        mock_open.return_value.read.return_value = json.dumps(resp_dict)
        with mock.patch.object(client.opener,
                               'open',
                               mock_open,
                               mocksignature=True):
            resp = client.get('payments')
        self.assertEqual(resp.json, resp_dict)
        mock_open.return_value.read.assert_called_once_with()

    def test_post(self):
        client = Client(**self.production_config)
        resp_body_dict = {'foo': 'bar'}
        mock_open = mock.mocksignature(client.opener.open)
        mock_resp = mock.Mock()
        mock_resp.read = mock.Mock(return_value=json.dumps(resp_body_dict))
        mock_open.mock.return_value = mock_resp
        with mock.patch.object(client.opener, 'open', new=mock_open):
            resp = client.post('payments', resp_body_dict)
        self.assertEqual(resp.json, resp_body_dict)

    def test_delete(self):
        client = Client(**self.production_config)
        mock_open = mock.mocksignature(client.opener.open)
        mock_resp = mock.Mock()
        mock_resp.read = mock.Mock(return_value=json.dumps({}))
        mock_open.mock.return_value = mock_resp
        with mock.patch.object(client.opener, 'open', new=mock_open):
            resp = client.delete('payments/sid')
        self.assertEqual(resp.json, {})

    def test_put(self):
        client = Client(**self.production_config)
        resp_body_dict = {'foo': 'bar'}
        mock_open = mock.mocksignature(client.opener.open)
        mock_resp = mock.Mock()
        mock_resp.read = mock.Mock(return_value=json.dumps(resp_body_dict))
        mock_open.mock.return_value = mock_resp
        with mock.patch.object(client.opener, 'open', new=mock_open):
            resp = client.put('payments/sid', resp_body_dict)
        self.assertEqual(resp.json, resp_body_dict)

class TestURLEncode(unittest.TestCase):

    def test_percentencodes(self):
        query = {'item': '$@!'}
        expected = 'item=%24%40%21'
        self.assertEqual(_url_encode(query), expected)

    def test_encodes_unicode(self):
        query = {'item': u'\u2603'}
        expected = 'item=%E2%98%83'
        self.assertEqual(_url_encode(query), expected)

    def test_encodes_dict(self):
        query = {
            'a': '1',
            'b': '2',
            'c': '3',
        }
        encoded = _url_encode(query)
        self.assertEqual(set(['a=1', 'b=2', 'c=3']), set(encoded.split('&')))

    def test_encodes_tuple_list(self):
        query = [
            ('a', '1'),
            ('b', '2'),
            ('c', '3'),
        ]
        encoded = _url_encode(query)
        self.assertEqual(encoded, 'a=1&b=2&c=3')

    def test_encodes_numbers(self):
        query = [
            ('a', 1),
            ('b', '2'),
            ('c', 3),
        ]
        encoded = _url_encode(query)
        self.assertEqual(encoded, 'a=1&b=2&c=3')

    def test_strips_none(self):
        query = [
            ('a', '1'),
            ('b', None),
            ('c', 3),
        ]
        encoded = _url_encode(query)
        self.assertEqual(encoded, 'a=1&c=3')

    def test_rejects_string_query(self):
        query = 'test'
        self.assertRaises(TypeError, _url_encode, query)
