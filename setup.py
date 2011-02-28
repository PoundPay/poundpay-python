try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='Poundpay',
    version='0.0.1',
    url='https://dev.poundpay.com/',
    license='BSD',
    author='Matin Tamizi',
    author_email='devsupport@poundpay.com',
    description='Payments platform for marketplaces',
    packages=['poundpay'],
    test_suite='nose.collector',
    install_requires=['simplejson']
)
