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
        amount=10000,   # in usd cents, not dollars
        payer_fee_amount=0,
        payer_email_address='fred@example.com',
        recipient_fee_amount=500,
        recipient_email_address='david@example.com',
        description='Beats by Dr. Dre',
    ).save()


Payment methods
```````````````

::

    list_of_payments = poundpay.Payment.all()
    payment = poundpay.Payment.find(payment_sid)
    payment.escrow()   # AUTHORIZED -> ESCROWED.  Credit card is charged
    payment.release()  # ESCROWED   -> RELEASED.  Recipient receives money
    payment.cancel()   # ESCROWED   -> CANCELED.  Payer receives refund
    

Serving the payment IFRAME
``````````````````````````

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
        payment_sid: "{{payment.sid}}",
        success: handlePaymentSuccess,
        error: handlePaymentError,
        first_name: "Fred", // Optional
        last_name: "Nietzsche", // Optional
        address_street: "990 Guerrero St", // Optional
        address_city: "San Francisco", // Optional
        address_state: "California", // Optional
        address_zip: "94110", // Optional
        server: "https://www-sandbox.poundpay.com"  // Exclude for production
      });
    </script>
    

Creating a Charge Permission
````````````````````````````

::

    charge_permission = poundpay.ChargePermission(
        email_address='payer@example.com',
    ).save()


Deactivating a Charge Permission
````````````````````````````````

::

    charge_permission = poundpay.ChargePermission.find(charge_permission_sid)
    charge_permission.deactivate()


ChargePermission methods
````````````````````````

::

    list_of_payments = poundpay.ChargePermission.all()
    charge_permission = poundpay.ChargePermission.find(charge_permission_sid)
    charge_permission.deactivate()  # CREATED or ACTIVE -> INACTIVE. Charge permission is deactivated and can no longer be used to authorize payments for the associated payer.
    

Serving the charge permission IFRAME
````````````````````````````````````

::

    <script src="https://www.poundpay.com/js/poundpay.js"></script>

    <div id="pound-root"></div>

    <script>
      function handleChargePermissionSuccess() {
        // do something
      }

      function handleChargePermissionError() {
        // handle error
      }

      PoundPay.init({
        charge_permission_sid: "{{charge_permission.sid}}",
        success: handleChargePermissionSuccess,
        error: handleChargePermissionError,
        name: "Freddy Nietzsche", // Optional
        address_street: "990 Guerrero St", // Optional
        address_city: "San Francisco", // Optional
        address_state: "California", // Optional
        address_zip: "94110", // Optional
        server: "https://www-sandbox.poundpay.com"  // Exclude for production
      });
    </script>
    
    
Batching
````````

In some cases you may wish to batch authorize and escrow a collection of
payments. By doing so there will be only *one* payer charge for that collection
of payments. Note that if you do batch authorize a collection of payments that
it must *also* be batch escrowed.

Batching is designed for shopping carts where you want a collection of payments
to appear to appear as a single charge.

In order to use batching you simply need to pass `sids` for *all* payments in
the collection you want to batch to the IFrame::

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
        payment_sid: [
            "{{payment1.sid}}"
            "{{payment2.sid}}",
            "{{payment3.sid}}"
            ],
        success: handlePaymentSuccess,
        error: handlePaymentError,
        first_name: "Fred", // Optional
        last_name: "Nietzsche", // Optional
        address_street: "990 Guerrero St", // Optional
        address_city: "San Francisco", // Optional
        address_state: "California", // Optional
        address_zip: "94110", // Optional
        server: "https://www-sandbox.poundpay.com"  // Exclude for production
      });
    </script>

Alternatively if you are directly authorizing the payments using a charge
permission::

    Payments.batch_update(
        payment1.sid, payment2.sid, payment3.sid,
        status='AUTHORIZED')

Finally you'll need to batch escrow the payments::

    Payments.batch_update(
        payment1.sid, payment2.sid, payment3.sid,
        status='ESCROWED')

Notice that if you did the following instead an error would be triggered since
batched payments *must* be authorized and escrowed collectively::

    Payments.find(payment1.sid, status='ESCROWED').save()  # fails

However if you cancel some of the payments prior to batch escrow you should
exclude them from the batch call::

    Payments.find(payment1.sid, status='CANCEL').save()  # ok

    Payments.batch_update(
        payment2.sid, payment3.sid,
        status='ESCROWED')

Links
`````

* `Developer Documentation <https://dev.poundpay.com/>`_
* `Website  <https://poundpay.com/>`_
