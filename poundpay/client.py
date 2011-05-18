import base64
import threading
import urllib2
from urllib import quote


try:
    import simplejson as json
except ImportError:
    import json

def _url_encode(query):
    """Version of url encoder which strips out None values and encodes
    Unicode as utf-8 before url-encoding.
    
    Logic partially copied from urllib.urlencode.
    """
    if hasattr(query, "items"):
        query = query.items() # convert a mapping object to a list of tuples
    else:
        try:
            # make sure query looks like a sequence of tuples (or looks empty)
            if len(query) and not isinstance(query[0], tuple):
                raise TypeError
        except TypeError:
            ty,va,tb = sys.exc_info()
            raise TypeError, "not a valid non-string sequence or mapping object", tb
    l = []
    for k, v in query:
        k = quote(str(k))
        if v is None:
            # skip None values
            continue
        elif isinstance(v, unicode):
            # encode unicode as utf-8
            v = quote(v.encode('utf-8'))
        else:
            v = quote(str(v))
        
        l.append('%s=%s' % (k, v))
    return '&'.join(l)

class ClientResponse(object):
    """The response returned from any :class:`~poundpay.Client` HTTP method.
    :class:`~poundpay.ClientResponse` has a ``response`` instance variable,
    representing the file-like object returned by `urllib2.urlopen <http://
    docs.python.org/library/urllib2.html#urllib2.urlopen>`_ and a ``data``
    instance variable, representing the raw data ``read()`` from the
    ``response``.

    Sample usage::

       response = urllib2.urlopen('http://google.com')
       client_response = ClientResponse(response, response.read())

       # access the internal response object for its API
       assert client_response.response.getcode() == 200
       assert client_response.response.geturl() == 'http://google.com'

       # access the internal data object for the read contents.
       assert 'html' in client_response.data.lower()

    """

    def __init__(self, file_like_object, data):
        self.response = file_like_object
        self.data = data

    @property
    def json(self):
        """A property which decodes a JSON payload.
        Equivalent to::

           return json.loads(self.data)

        """

        return json.loads(self.data)


class Client(threading.local):
    """Client is a thread-local object that is instantiated as a class
    variable of :class:`~poundpay.Resource`, particularly when
    :func:`~poundpay.configure` is used.

    Instantiating :class:`~poundpay.Client` is as simple as
    passing in your developer's ``developer_sid`` and
    ``auth_token``.

    The ``opener_handlers`` parameter should be an iterable to allow
    for custom handlers to pass into `urllib2.build_opener()
    <http://docs.python.org/library/urllib2.html#urllib2.build_opener>`_.

    """
    #: The API URL to use for all HTTP requests
    API_URL = 'https://api.poundpay.com'

    #: The API version to use for all HTTP requests. PoundPay's current
    #: version can always be found at the `Developer website
    #: <https://dev.poundpay.com/>`_
    API_VERSION = 'silver'

    def __init__(self, developer_sid, auth_token, api_url=API_URL,
                 api_version=API_VERSION, opener_handlers=None):
        if not (developer_sid and auth_token):
            raise ValueError('developer_sid and auth_token required')
        if not developer_sid.startswith('DV'):
            raise ValueError('developer_sid must start with DV')

        if not api_url:
            api_url = Client.API_URL

        if not api_version:
            api_version = Client.API_VERSION

        self.base_url = '%s/%s/' % (api_url, api_version)
        self.developer_sid = developer_sid

        opener_handlers = opener_handlers if opener_handlers else []
        self.opener = urllib2.build_opener(*opener_handlers)
        authstring = base64.b64encode('%s:%s' % (developer_sid, auth_token))
        self.opener.addheaders.append(('Authorization', 'Basic ' + authstring))

    def get(self, path, **params):
        """Issue a ``GET /path/``. If the ``/path/`` has a resource-sid
        associated with it, this will return the representation of the
        resource located at ``/path/`` that has that associated resource-sid.

        :param path: The resource location
        :param params: Optional parameters to `urllib.urlencode <http://docs.
           python.org/library/urllib.html#urllib.urlencode>`_ and append to
           ``path`` prefixed with a '?'.
        :rtype: A :class:`~poundpay.ClientResponse`.

        ::

           # issue an index on all our payments
           client = Client('YOUR_DEVELOPER_SID', 'YOUR_AUTH_TOKEN')
           client_response = client.get('/silver/payments/')
           assert client_response.response.getcode() == 200
           # gives us back a paginated response
           payload = client_response.json
           assert 'num_pages' in payload
           assert 'page_size' in payload
           assert 'payments' in payload   # will be the resource name

           # show a resource with resource-sid PY...
           client_response = client.get('/silver/payments/PY...')
           assert client_response.response.getcode() == 200
           assert isinstance(client_response.json, dict)
           assert client_response.json['sid'] == 'PY...'

        """
        if params:
            params = _url_encode(params)
            path = path.rstrip('/') + '/?' + params
        req = urllib2.Request(self.base_url + path)
        resp = self.opener.open(req)
        return ClientResponse(resp, resp.read())

    def post(self, path, params):
        """Issue a ``POST /path/``.

        :param path: The resource location
        :param params: The parameters to create the resource with.
        :rtype: A :class:`~poundpay.ClientResponse`.

        ::

           client = Client('YOUR_DEVELOPER_SID', 'YOUR_AUTH_TOKEN')
           data = {
              'amount': 4000,
              'payer_email_address': 'x@y.org',
              'recipient_email_address': 'bl@x.com',
              'payer_fee_amount': 100,
              'recipient_fee_amount': 0,
           }
           client_response = client.post('/silver/payments', data)
           assert client_response.response.getcode() == 201
           assert isinstance(client_response.json, dict)
           for key, value in data.iteritems():
               assert client_response.json[key] == value

        """
        data = _url_encode(params)
        req = urllib2.Request(self.base_url + path, data)
        resp = self.opener.open(req)
        return ClientResponse(resp, resp.read())

    def put(self, path, params):
        """Issue a ``PUT /path/resource-sid``.

        :param path: The resource location + the resource's sid
        :param params: The parameters to update the resource with.
        :rtype: A :class:`~poundpay.ClientResponse`.

        ::

           client = Client('YOUR_DEVELOPER_SID', 'YOUR_AUTH_TOKEN')
           data = {'status': 'CANCELED'}
           client_response = client.put('/silver/payments/PY...', data)
           assert client_response.response.getcode() == 201
           assert isinstance(client_response.json, dict)
           assert client_response.json['status'] == 'CANCELED'

        """

        data = _url_encode(params)
        req = urllib2.Request(self.base_url + path, data)
        req.get_method = lambda: 'PUT'
        resp = self.opener.open(req)
        return ClientResponse(resp, resp.read())

    def delete(self, path):
        """Issue a ``DELETE /path/resource-sid``.

        :param path: The resource location + the resource's sid
        :rtype: A :class:`~poundpay.ClientResponse`.

        ::

           client = Client('YOUR_DEVELOPER_SID', 'YOUR_AUTH_TOKEN')
           client_response = client.delete('/silver/payments/PY...')
           assert client_response.response.getcode() == 204
           assert client_response.json == {}

        """

        req = urllib2.Request(self.base_url + path)
        req.get_method = lambda: 'DELETE'
        resp = self.opener.open(req)
        return ClientResponse(resp, resp.read())
