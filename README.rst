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

    payment = poundpay.Payment(
        amount=10000,
        payer_fee_amount=0,
        payer_email_address='fred@example.com',
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
        server: "https://www-sandbox.poundpay.com"  // Exclude for production
      });
    </script>


Payment methods
```````````````

::

    list_of_payments = poundpay.Payment.all()
    payment = poundpay.Payment.find(payment_sid)
    payment.escrow()   # AUTHORIZED -> ESCROWED.  Credit card is charged
    payment.release()  # ESCROWED   -> RELEASED.  Recipient receives money
    payment.cancel()   # ESCROWED   -> CANCELED.  Payer receives refund


Links
`````

* `Developer Documentation <https://dev.poundpay.com/>`_
* `Website  <https://poundpay.com/>`_