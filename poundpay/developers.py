from .resource import Resource


class Developer(Resource):
    _name = 'developers'

    @classmethod
    def find_me(cls):
        return cls.find(cls.client.developer_sid)
