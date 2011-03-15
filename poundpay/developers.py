from .resource import Resource


class Developer(Resource):
    _name = 'developers'

    @classmethod
    def find_me(cls):
        return cls.find(cls._client.developer_sid)
