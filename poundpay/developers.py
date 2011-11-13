from .resource import Resource


class Developer(Resource):
    """The Developer resource, represented by a RESTful resource located at
    ``/developers``.

    """
    _name = 'developers'

    @classmethod
    def find_me(cls):
        """Issue a ``GET /developers/<developer_sid>``

        ::

           developer = poundpay.Developer.find_me()
           assert developer.sid == 'YOUR_DEVELOPER_SID'
           developer.callback_url = 'http://marketplace.com/callback/'
           developer.charge_permissioncallback_url = 'http://marketplace.com/charge_permission_callback/'
           developer.save()
           developer = poundpay.Developer.find_me()
           assert developer.callback_url == 'http://marketplace.com/callback/'
           assert developer.callback_url == 'http://marketplace.com/charge_permission_callback/'

        """
        return cls.find(cls.client.developer_sid)
