try:
    import simplejson as json
except ImportError:
    import json
import threading
from urllib import urlencode
import urllib2


class Client(threading.local):
    API_URL = 'https://api.poundpay.com'
    API_VERSION = 'silver'

    def __init__(self, developer_sid, auth_token, api_url=API_URL,
                 api_version=API_VERSION):
        self.base_url = '{}/{}'.format(api_url, api_version)
        self.developer_sid = developer_sid

        # Use Python's default basic auth handler.  The problem here is that
        # it makes an extra round-trip everytime to determine if the request
        # requires authentication
        password_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
        password_manager.add_password(None, api_url, developer_sid, auth_token)
        auth_handler = urllib2.HTTPBasicAuthHandler(password_manager)

        self.opener = urllib2.build_opener(auth_handler)

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
