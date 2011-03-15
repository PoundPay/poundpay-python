from .client import Client
from .developers import Developer
from .resource import Resource
from .payments import Payment


__all__ = ['Client', 'Developer', 'Resource', 'Payment']


def configure(developer_sid, auth_token, api_url=None, api_version=None):
    Resource._client = Client(developer_sid, auth_token, api_url, api_version)
