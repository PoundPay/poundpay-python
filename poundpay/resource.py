class Resource(object):
    """Class that represents a RESTful resource at a particular endpoint.
    Has a class variable, :class:`~poundpay.Client`, that is defaulted to
    ``None``. Once configured, there are standard operators that are
    enabled on any resource.

    """
    #: client is the class variable representing a :class:`~poundpay.Client`
    client = None
    #: _name is the pluralized name of a resource represented by a descendant
    #: of :class:`~poundpay.Resource`.
    _name = None

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        attrs = ', '.join(['%s=%s' % (k, repr(v)) for k, v in
                           self.__dict__.iteritems()])
        return '%s(%s)' % (self.__class__.__name__, attrs)

    @classmethod
    def all(cls, **params):
        """Represents an index of a resource by issuing a ``GET /resource/``

        :param params: Optional parameters to `urllib.urlencode <http://docs.
           python.org/library/urllib.html#urllib.urlencode>`_ and append to
           ``/resource/`` prefixed with a '?'.
        :rtype: A list of :class:`~poundpay.Resource` descendants,
           represented by ``cls``.

        Sample Usage::

           import poundpay
           poundpay.configure('DEVELOPER_SID', 'AUTH_TOKEN')

           # paginated fetch of all associated payments
           # equivalent of GET /silver/payments/
           poundpay.Payment.all()

           # fetch by offset and give me 5 results
           # equivalent of GET /silver/payments/?offset=10&limit=5
           poundpay.Payment.all(offset=10, limit=5)

        """
        resp = cls.client.get(cls._name, **params)
        return [cls(**attrs) for attrs in resp.json[cls._name]]

    @classmethod
    def find(cls, sid, **params):
        """Represents an show of a resource by issuing a
        ``GET /resource/sid``

        :param sid: Represents the identifier of a resource
        :param params: Optional parameters to `urllib.urlencode <http://docs.
           python.org/library/urllib.html#urllib.urlencode>`_ and append to
           ``/resource/sid`` prefixed with a '?'.
        :rtype: A :class:`~poundpay.Resource` descendant, represented
           by ``cls``.

        Sample Usage::

           import poundpay
           poundpay.configure('DEVELOPER_SID', 'AUTH_TOKEN')

           # paginated fetch of all associated payments
           # equivalent of GET /silver/payments/PY...
           poundpay.Payment.find('PY...')

        """
        resp = cls.client.get(cls._get_path(sid), **params)
        return cls(**resp.json)

    def save(self):
        """Issues either a ``POST`` or a ``PUT`` on a resource depending
        if has a ``sid`` or an ``id``.

        :rtype: A :class:`~poundpay.Resource` descendant, represented
           by ``cls``.

        Sample Usage::

           import poundpay
           poundpay.configure('DEVELOPER_SID', 'AUTH_TOKEN')

           # paginated fetch of all associated payments
           # equivalent of GET /silver/payments/
           data = {
              'amount': 4000,
              'payer_email_address': 'x@y.org',
              'recipient_email_address': 'bl@x.com',
              'payer_fee_amount': 100,
              'recipient_fee_amount': 0,
           }
           payment = poundpay.Payment(**data)
           payment.save()   # issues POST /silver/payments
           assert payment.sid.startswith('PY')
           payment.state = 'CANCELED'
           # because payment already has a sid
           payment.save()   # issues PUT /silver/payments

        """
        if hasattr(self, 'sid'):
            attrs = self._update(**self.__dict__)
        else:
            attrs = self._create(**self.__dict__)
        self.__dict__.update(attrs)
        return self

    def delete(self):
        """Issues a ``DELETE`` on a resource.

        :rtype: None

        Sample Usage::

           import poundpay
           poundpay.configure('DEVELOPER_SID', 'AUTH_TOKEN')
           payment = poundpay.Payment.find('PY...')
           payment.delete()   # issues a DELETE /silver/payments/PY...
           payment = poundpay.Payment.find('PY...')
           assert payment.response.getcode() == 404

        """
        self.client.delete(self._get_path(self.sid))

    @classmethod
    def _update(cls, sid, **attrs):
        resp = cls.client.put(cls._get_path(sid), attrs)
        return resp.json

    @classmethod
    def _create(cls, **attrs):
        resp = cls.client.post(cls._name, attrs)
        return resp.json

    @classmethod
    def _get_path(cls, sid):
        return '%s/%s' % (cls._name, sid)
