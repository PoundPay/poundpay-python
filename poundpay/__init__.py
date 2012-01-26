
from .client import Client, ClientResponse, ClientException
from .developers import Developer
from .resource import Resource
from .payments import Payment
from .charge_permissions import ChargePermission
from .users import User


__all__ = [
    'Client', 'ClientResponse', 'Developer', 'Resource', 'Payment',
    'User', 'ChargePermission',
    ]


def configure(developer_sid, auth_token, api_url=None, api_version=None):
    """Configure a static client object.

    :param developer_sid: Your developer sid
    :param auth_token: Your designated authentication token (keep this secret)
    :param api_url: The API URL to hit. Defaults to ``Client.API_URL`` when
       client is configured.
    :param api_version: The API Version. Defaults to ``Client.API_VERSION``
       when client is configured.

    ::

       import poundpay
       poundpay.configure('YOUR_DEVELOPER_SID', 'YOUR_AUTH_TOKEN')

       developer = poundpay.Developer.find_me()
       assert developer.sid == 'YOUR_DEVELOPER_SID'

    """
    if not api_url:
        api_url = Client.API_URL

    if not api_version:
        api_version = Client.API_VERSION

    Resource.client = Client(developer_sid, auth_token, api_url, api_version)
