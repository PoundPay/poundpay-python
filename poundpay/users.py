from .resource import Resource


class User(Resource):
    """The User resource, represented by a RESTful resource located at
    ``/users``.

    """
    _name = 'users'
