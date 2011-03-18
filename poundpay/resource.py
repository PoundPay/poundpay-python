class Resource(object):
    client = None

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        attrs = ', '.join(['%s=%s' % (k, repr(v)) for k, v in
                           self.__dict__.iteritems()])
        return '%s(%s)' % (self.__class__.__name__, attrs)

    @classmethod
    def all(cls, **params):
        resp = cls.client.get(cls._name, **params)
        return [cls(**attrs) for attrs in resp.json[cls._name]]

    @classmethod
    def find(cls, sid, **params):
        resp = cls.client.get(cls._get_path(sid), **params)
        return cls(**resp.json)

    def save(self):
        if hasattr(self, 'sid'):
            attrs = self._update(**self.__dict__)
        else:
            attrs = self._create(**self.__dict__)
        self.__dict__.update(attrs)
        return self

    def delete(self):
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
