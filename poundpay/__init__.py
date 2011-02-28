from .client import Client
from .developers import Developer
from .resource import Resource
from .payments import Payment


__all__ = ['Client', 'Developer', 'Resource', 'Payment']


def configure(**config):
    Resource.client = Client(**config)
