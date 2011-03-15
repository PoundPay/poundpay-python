"""
PoundPay
--------

PoundPay enables developers to build apps which facilitate
transactions between two of their users. PoundPay is designed
specifically for these types of transactions, as opposed to direct
payments from customer to business. In short, PoundPay is the payments
platform for marketplaces.

Install
```````

::

    $ easy_install poundpay

Configure
`````````

::

    CONFIG = {
        'sandbox': {
            'developer_sid': 'DV0383d447360511e0bbac00264a09ff3c',
            'auth_token': ('c31155b9f944d7aed204bdb2a253fef13b4fdcc6ae15402004'
                           '49cc4526b2381a'),
            'www_url': 'https://www-sandbox.poundpay.com',
            'api_url': 'https://api-sandbox.poundpay.com'
        },
        'production': {
            'developer_sid': 'DV8dd93f0f3c6411e0863f00264a09ff3c',
            'auth_token': ('d8c4ea1bafd3fcac8c1062a72c22bcdb09321deb1041df2571'
                           '65cd6449def0de')
        }
    }

    import poundpay
    poundpay.configure(**CONFIG['production'])

Creating a Payment
``````````````````

::

    payment = Payment(
        amount=20000,
        payer_fee_amount=0,
        payer_email_address='fred@example.com',
        payer_sid='97f51e5c38e211e08625e7af17bae06a',  # Optional
        recipient_fee_amount=500,
        recipient_email_address='david@example.com',
        description='Beats by Dr. Dre',
    ).save()

Serving IFRAME
``````````````

::

    <script src="https://www.poundpay.com/js/poundpay.js"></script>

    <div id="pound-root"></div>

    <script>
      function handlePaymentSuccess() {
        // do something
      }

      function handlePaymentError() {
        // handle error
      }

      PoundPay.init({
        payment_sid: {{payment.sid}},
        success: handlePaymentSuccess,
        error: handlePaymentError,
        cardholder_name: "Fred Nietzsche", // Optional
        phone_number: "4085551234", // Optional
        server: "https://www-sandbox.poundpay.com"  // Exclude for production
      });
    </script>

Links
`````

* `Developer Documentation <https://dev.poundpay.com/>`_
* `Website  <https://poundpay.com/>`_

"""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='Poundpay',
    version='0.0.5',
    url='https://dev.poundpay.com/',
    license='BSD',
    author='Matin Tamizi, Mahmoud Abdelkader',
    author_email='devsupport@poundpay.com',
    description='Payments platform for marketplaces',
    long_description=__doc__,
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
