IFRAME_ROOT_URI = 'https://www-sandbox.poundpay.com'

DEV = dict(
    credentials=dict(
        developer_sid='DVb956191e242111e08016123140005921',
        auth_token='3af5f79f0672f203cbabc9b75f8bd6cc379f61409092bd514709ccb6721d970d',
        api_url='http://localhost:8000',
        ),
    IFRAME_ROOT_URI='http://localhost:5000',
    )

SANDBOX = dict(
    credentials=dict(             
        developer_sid='DV1adf7e34140711e1b97212314000d16f',
        auth_token='2b62669d5dc666113e06036c026624e1277171275c318965ed0d8d343fc02b09',
        api_url='https://api-sandbox.poundpay.com',
        ),
    IFRAME_ROOT_URI='https://www-sandbox.poundpay.com',
    )


PROD = dict(
    credentials=dict(             
        developer_sid='DVb956191e242111e08016123140005921',
        auth_token='3af5f79f0672f203cbabc9b75f8bd6cc379f61409092bd514709ccb6721d970d',
        api_url='https://api.poundpay.com',
        ),
    IFRAME_ROOT_URI='https://www.poundpay.com',
    )


DOCS = dict(
    credentials=dict(             
        developer_sid='DV1adf7e34140711e1b97212314000d16f',
        auth_token='2b62669d5dc666113e06036c026624e1277171275c318965ed0d8d343fc02b09',
        api_url='https://api-sandbox.poundpay.com',
        ),
    IFRAME_ROOT_URI='https://www-sandbox.poundpay.com',
    )


DEFAULT_PAYMENT = dict(
    amount='111',  # in usd cents
    payer_fee_amount='13',  # in usd cents
    recipient_fee_amount='32',  # in usd cents
    payer_email_address='andrew+hi@poundpay.com',
    recipient_email_address='andrew+bye@poundpay.com',
    description='Some Nutti Junk',
    developer_identifier='',
    )


SECRET_KEY = b'super secret key'


def get_credentials_for_env(environment):
    global IFRAME_ROOT_URI
    configurations = {
        'SANDBOX': SANDBOX,
        'DOCS': DOCS,
        'DEV': DEV,
        'PROD': PROD,
        }
    environment = environment.upper()
    configuration = configurations[environment]
    IFRAME_ROOT_URI = configuration['IFRAME_ROOT_URI']
    return configuration['credentials']
