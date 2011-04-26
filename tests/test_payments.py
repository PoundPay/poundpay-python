import unittest

import mock

from poundpay.payments import Payment


class TestPayment(unittest.TestCase):

    def test_escrow_throws_exception_if_not_AUTHORIZED(self):
        pass

    def test_release_throws_exception_if_not_ESCROWED(self):
        pass

    def test_cancel_throws_exception_if_not_ESCROWED(self):
        pass

    def test_cancel_sets_status_to_cancel_and_issues_save(self):
        pass

    def test_release_sets_status_to_released_and_issues_save(self):
        pass

    def test_escrow_sets_status_to_escrowed_and_issues_save(self):
        pass
