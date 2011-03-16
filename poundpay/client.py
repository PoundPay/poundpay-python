import base64
import threading
import urllib2
from urllib import urlencode


try:
    import simplejson as json
except ImportError:
    import json


class Client(threading.local):

    API_URL = 'https://api.poundpay.com'
    API_VERSION = 'silver'

    def __init__(self, developer_sid, auth_token, api_url=API_URL,
                 api_version=API_VERSION):
        if not (developer_sid and auth_token):
            raise ValueError('developer_sid and auth_token required')
        if not developer_sid.startswith('DV'):
            raise ValueError('developer_sid must start with DV')

        self.base_url = '%s/%s/' % (api_url, api_version)
        self.developer_sid = developer_sid

        self.opener = urllib2.build_opener()
        authstring = base64.b64encode('%s:%s' % (developer_sid, auth_token))
        self.opener.addheaders.append(('Authorization', 'Basic ' + authstring))

    def get(self, path):
        req = urllib2.Request(self.base_url + path)
        resp = self.opener.open(req)
        resp.body = resp.read()
        resp.json = json.loads(resp.body)
        return resp

    def post(self, path, params):
        data = urlencode(params)
        req = urllib2.Request(self.base_url + path, data)
        resp = self.opener.open(req)
        resp.body = resp.read()
        resp.json = json.loads(resp.body)
        return resp

    def put(self, path, params):
        data = urlencode(params)
        req = urllib2.Request(self.base_url + path, data)
        req.get_method = lambda: 'PUT'
        resp = self.opener.open(req)
        resp.body = resp.read()
        resp.json = json.loads(resp.body)
        return resp

    def delete(self, path):
        req = urllib2.Request(self.base_url + path)
        req.get_method = lambda: 'DELETE'
        resp = self.opener.open(req)
        return resp
