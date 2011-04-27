import unittest

import mock

import poundpay
from poundpay.payments import Payment


PAYMENT_STATUSES = frozenset([
    'STAGED',
    'AUTHORIZED',
    'ESCROWED',
    'CANCELED',
    'RELEASED',
    'REFUNDED',
    'UNDER_REVIEW',
    'REJECTED',
])


class TestPayment(unittest.TestCase):

    def setUp(self):
        poundpay.configure(**self.config)

    @property
    def config(self):
        return {'developer_sid': 'DVxxx', 'auth_token': 'AUTH_TOKEN'}

    @property
    def payment_arguments(self):
        return {
            'amount': 500,
            'description': u'A description',
            'developer_sid': u'DVxxx',
            'payer_email_address': u'payer@example.com',
            'payer_fee_amount': 200,
            'recipient_email_address': u'recipient@example.com',
            'recipient_fee_amount': 0,
            'sid': u'PYxxx',
        }

    def test_escrow_throws_exception_if_not_AUTHORIZED(self):
        payment = Payment(**self.payment_arguments)
        for status in PAYMENT_STATUSES:
            if status == 'AUTHORIZED':
                continue
            payment.status = status
            with self.assertRaises(poundpay.payments.PaymentEscrowError):
                payment.escrow()

    def test_release_throws_exception_if_not_ESCROWED(self):
        payment = Payment(**self.payment_arguments)
        for status in PAYMENT_STATUSES:
            if status == 'ESCROWED':
                continue
            payment.status = status
            with self.assertRaises(poundpay.payments.PaymentReleaseError):
                payment.release()

    def test_cancel_throws_exception_if_not_ESCROWED(self):
        payment = Payment(**self.payment_arguments)
        for status in PAYMENT_STATUSES:
            if status == 'ESCROWED':
                continue
            payment.status = status
            with self.assertRaises(poundpay.payments.PaymentCancelError):
                payment.cancel()

    def test_cancel_sets_status_to_cancel_and_issues_save(self):
        kwargs = self.payment_arguments
        kwargs['status'] = 'ESCROWED'
        payment = Payment(**kwargs)
        with mock.patch.object(Payment, 'save') as patched_save:
            payment.cancel()

        patched_save.assert_called_once_with()
        self.assertEqual(payment.status, 'CANCELED')

    def test_release_sets_status_to_released_and_issues_save(self):
        kwargs = self.payment_arguments
        kwargs['status'] = 'ESCROWED'
        payment = Payment(**kwargs)
        with mock.patch.object(Payment, 'save') as patched_save:
            payment.release()

        patched_save.assert_called_once_with()
        self.assertEqual(payment.status, 'RELEASED')

    def test_escrow_sets_status_to_escrowed_and_issues_save(self):
        kwargs = self.payment_arguments
        kwargs['status'] = 'AUTHORIZED'
        payment = Payment(**kwargs)
        with mock.patch.object(Payment, 'save') as patched_save:
            payment.escrow()

        patched_save.assert_called_once_with()
        self.assertEqual(payment.status, 'ESCROWED')
