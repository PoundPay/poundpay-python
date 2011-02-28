try:
    import simplejson as json
except ImportError:
    import json


class Resource(object):
    client = None

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        attrs = ', '.join(['{}={}'.format(k, repr(v)) for k, v in
                           self.__dict__.iteritems()])
        return '{classname}({attrs})'.format(
            classname=self.__class__.__name__ ,
            attrs=attrs)

    @classmethod
    def all(cls):
        resp = cls.client.get(cls._path)
        return [cls(**attrs) for attrs in resp.json[cls._name]]

    @classmethod
    def find(cls, sid):
        resp = cls.client.get(cls._path + sid)
        return cls(**resp.json)

    def save(self):
        if hasattr(self, 'sid'):
            attrs = self._update(**self.__dict__)
        else:
            attrs = self._create(**self.__dict__)
        self.__dict__.update(attrs)
        return self

    def delete(self):
        self.client.delete(cls._path + sid)

    @classmethod
    def _update(cls, sid, **attrs):
        resp = cls.client.put(cls._path + sid, attrs)
        return resp.json

    @classmethod
    def _create(cls, **attrs):
        resp = cls.client.post(cls._path, attrs)
        return resp.json
