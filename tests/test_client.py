import os
import json
import unittest

import mock

from poundpay.client import (
    Client, ClientResponse, _url_encode, ClientException
    )


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

    def test_str(self):
        response = mock.Mock()
        response.msg = 'OK'
        response.getcode.return_value = '200'
        client_response = ClientResponse(
            response,
            json.dumps({'foo': 'bar'})
            )
        self.assertEqual(
            str(client_response), "[200 OK] - {'foo': 'bar'}"
            )


PRODUCTION_CONFIG = {
    'developer_sid': 'DV0383d447360511e0bbac00264a09ff3c',
    'auth_token': 'c31155b9f944d7aed204bdb2a253fef13b4fdcc6ae15402004',
    }


SANDBOX_CONFIG = {
    'developer_sid': 'DV0383d447360511e0bbac00264a09ff3c',
    'auth_token': 'c31155b9f944d7aed204bdb2a253fef13b4fdcc6ae15402004',
    'api_url': 'https://api-sandbox.poundpay.com',
    'api_version': 'gold',
    }


class TestClient(unittest.TestCase):

    def test_developer_sid_and_auth_token_required(self):
        with self.assertRaises(ValueError):
            Client('DV', None)

    def test_developer_sid_starts_with_DV(self):
        config = PRODUCTION_CONFIG
        with self.assertRaises(ValueError):
            Client(config['auth_token'], config['developer_sid'])

    def test_default_api_version_when_explicity_set_to_None(self):
        config = PRODUCTION_CONFIG
        config['api_version'] = None
        client = Client(**config)
        self.assertTrue(client.base_url.endswith(Client.API_VERSION + '/'))

    def test_default_api_url_when_explicity_set_to_None(self):
        config = PRODUCTION_CONFIG
        config['api_url'] = None
        client = Client(**config)
        self.assertTrue(client.base_url,
                        os.path.join(client.API_URL, client.API_VERSION))

    def test_default_url_and_version(self):
        client = Client(**PRODUCTION_CONFIG)
        self.assertEqual(client.base_url,
                         'https://api.poundpay.com/silver/')
        self.assertIn('Authorization', dict(client.opener.addheaders))
        authstring = dict(client.opener.addheaders)['Authorization'][6:]
        developer_sid, auth_token = authstring.decode('base64').split(':')
        self.assertEqual(developer_sid, PRODUCTION_CONFIG['developer_sid'])
        self.assertEqual(auth_token, PRODUCTION_CONFIG['auth_token'])

    def test_different_url_and_version(self):
        client = Client(**SANDBOX_CONFIG)
        self.assertEqual(client.base_url,
                         'https://api-sandbox.poundpay.com/gold/')


class TestClientHTTPOperation(unittest.TestCase):

    def setUp(self):
        self.client = Client(**PRODUCTION_CONFIG)
        self.resp_dict = {'foo': 'bar'}
        self.mock_open = mock.Mock()
        self.mock_open.return_value.read.return_value = json.dumps(
            self.resp_dict
            )

    def test_get(self):
        with mock.patch.object(
                self.client.opener, 'open', self.mock_open, mocksignature=True
                ):
            resp = self.client.get('payments')
        self.assertEqual(resp.json, self.resp_dict)
        self.mock_open.return_value.read.assert_called_once_with()

    def test_http_error(self):
        response = mock.Mock()
        response.code = 403
        response.msg = 'Unauthorized'
        response.info.return_value = {}
        response.read.return_value = json.dumps({'message': 'unauthorized yo'})
        response_handler = mock.Mock()
        response_handler.default_open.return_value = response
        self.client.opener.handle_open['default'] = [response_handler]
        with self.assertRaises(ClientException) as exception:
            self.client.post('payments', self.resp_dict)
        exc = exception.exception
        self.assertEqual(
            str(exc.args[0]), ("HTTP Error 403: Unauthorized :: "
                               "{'message': 'unauthorized yo'}")
            )

    def test_http_success(self):
        response = mock.Mock()
        response.code = 200
        response.getcode.return_value = response.code
        response.msg = 'OK'
        response.info.return_value = {}
        response.read.return_value = json.dumps({'hi': 'there'})
        response_handler = mock.Mock()
        response_handler.default_open.return_value = response
        self.client.opener.handle_open['default'] = [response_handler]
        resp = self.client.post('payments', self.resp_dict)
        self.assertEqual(
            str(resp), "[200 OK] - {'hi': 'there'}"
            )

    def test_post(self):
        with mock.patch.object(
                self.client.opener, 'open', self.mock_open, mocksignature=True
                ):
            resp = self.client.post('payments', self.resp_dict)
        self.assertEqual(resp.json, self.resp_dict)

    def test_delete(self):
        self.mock_open.return_value.read.return_value = json.dumps({})
        with mock.patch.object(
                self.client.opener, 'open', self.mock_open, mocksignature=True
                ):
            resp = self.client.delete('payments/sid')
        self.assertEqual(resp.json, {})

    def test_put(self):
        with mock.patch.object(
                self.client.opener, 'open', self.mock_open, mocksignature=True
                ):
            resp = self.client.put('payments/sid', self.resp_dict)
        self.assertEqual(resp.json, self.resp_dict)


class TestClientHTTPOperationWithHeaders(unittest.TestCase):

    def test_get_pass_header(self):
        client = Client(**PRODUCTION_CONFIG)
        resp_dict = {'foo': 'bar'}
        mock_open = mock.Mock()
        mock_open.return_value.read.return_value = json.dumps(resp_dict)
        resp_header = {'foo': 'bar'}
        with mock.patch.object(client.opener,
                               'open',
                               mock_open,
                               mocksignature=True), \
             mock.patch('poundpay.client.urllib2') as urllib2_mock:
            resp = client.get('payments', resp_header)
        _args, kwargs = urllib2_mock.Request.call_args
        self.assertEqual(resp.json, resp_dict)
        self.assertEqual(kwargs['headers'], resp_header)
        mock_open.return_value.read.assert_called_once_with()

    def test_post_pass_header(self):
        client = Client(**PRODUCTION_CONFIG)
        resp_body_dict = {'foo': 'bar'}
        mock_open = mock.mocksignature(client.opener.open)
        mock_resp = mock.Mock()
        mock_resp.read = mock.Mock(return_value=json.dumps(resp_body_dict))
        mock_open.mock.return_value = mock_resp
        resp_header = {'foo': 'bar'}
        with mock.patch.object(client.opener, 'open', new=mock_open), \
             mock.patch('poundpay.client.urllib2') as urllib2_mock:
            resp = client.post('payments', resp_body_dict, resp_header)
        _args, kwargs = urllib2_mock.Request.call_args
        self.assertEqual(kwargs['headers'], resp_header)
        self.assertEqual(resp.json, resp_body_dict)

    def test_delete_pass_header(self):
        client = Client(**PRODUCTION_CONFIG)
        mock_open = mock.mocksignature(client.opener.open)
        mock_resp = mock.Mock()
        mock_resp.read = mock.Mock(return_value=json.dumps({}))
        mock_open.mock.return_value = mock_resp
        resp_header = {'foo': 'bar'}
        with mock.patch.object(client.opener, 'open', new=mock_open), \
             mock.patch('poundpay.client.urllib2') as urllib2_mock:
            resp = client.delete('payments/sid', resp_header)
        _args, kwargs = urllib2_mock.Request.call_args
        self.assertEqual(kwargs['headers'], resp_header)
        self.assertEqual(resp.json, {})

    def test_put_pass_header(self):
        client = Client(**PRODUCTION_CONFIG)
        resp_body_dict = {'foo': 'bar'}
        mock_open = mock.mocksignature(client.opener.open)
        mock_resp = mock.Mock()
        mock_resp.read = mock.Mock(return_value=json.dumps(resp_body_dict))
        mock_open.mock.return_value = mock_resp
        resp_header = {'foo': 'bar'}
        with mock.patch.object(client.opener, 'open', new=mock_open), \
             mock.patch('poundpay.client.urllib2') as urllib2_mock:
            resp = client.put('payments/sid', resp_body_dict, resp_header)
        _args, kwargs = urllib2_mock.Request.call_args
        self.assertEqual(kwargs['headers'], resp_header)
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
        with self.assertRaises(ValueError) as exc:
            _url_encode('test')

        exception = exc.exception
        self.assertEqual(exception.message, 'need more than 1 value to unpack')

    def test_multi_query_dict_support(self):
        query = [
            ('a', '1'),
            ('a', '2'),
        ]
        encoded = _url_encode(query)
        self.assertEqual(encoded, 'a=1&a=2')
