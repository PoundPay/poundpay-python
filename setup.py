"""
PoundPay Python client library.

See ``readme.rst`` for usage advice.

"""
import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


PATH_TO_FILE = os.path.dirname(__file__)


with open(os.path.join(PATH_TO_FILE, 'README.rst')) as f:
    long_description = f.read()


setup(
    name='Poundpay',
    version='0.5.1',
    url='https://dev.poundpay.com/',
    license='BSD',
    author='Matin Tamizi, Mahmoud Abdelkader',
    author_email='devsupport@poundpay.com',
    description='Payments platform for marketplaces',
    long_description=long_description,
    packages=['poundpay'],
    install_requires=[
        'simplejson',
    ],
    test_suite='nose.collector',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
