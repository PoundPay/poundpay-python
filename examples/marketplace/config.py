IFRAME_ROOT_URI = 'https://www-sandbox.poundpay.com'


SANDBOX = dict(
    credentials=dict(             
        developer_sid='DVxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
        auth_token='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',                     
        api_url='https://api-sandbox.poundpay.com',
        ),
    IFRAME_ROOT_URI='https://www-sandbox.poundpay.com',
    )


DEFAULT_PAYMENT = dict(
    amount='20011',  # in usd cents
    payer_fee_amount='123',  # in usd cents
    recipient_fee_amount='321',  # in usd cents
    payer_email_address='fred@example.com',
    recipient_email_address='immanuel@example.com',
    description='Beats by Dr. Dre (White)',
    developer_identifier='',
    )


SECRET_KEY = b'super secret key'


def get_credentials_for_env(environment):
    global IFRAME_ROOT_URI
    configurations = {
        'SANDBOX': SANDBOX,
        }
    environment = environment.upper()
    configuration = configurations[environment]
    IFRAME_ROOT_URI = configuration['IFRAME_ROOT_URI']
    return configuration['credentials']
