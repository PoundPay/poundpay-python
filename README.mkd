=====
Poundpay
=====

Poundpay is a payments platform for marketplaces

Install
-------

    pip install poundpay



Configure
---------

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
-----------------

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
--------------

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
