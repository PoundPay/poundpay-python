"""
PoundPay Python client library.

See ``readme.rst`` for usage advice.

"""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as f:
    long_description = f.read()


setup(
    name='Poundpay',
    version='0.1.0',
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
