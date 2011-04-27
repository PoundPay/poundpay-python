import unittest

import mock

from poundpay.resource import Resource


class TestResource(unittest.TestCase):

    def test_resource_constructor_updates__dict__(self):
        resource_args = {'sid': 1, 'blah': 2}
        resource = Resource(**resource_args)
        self.assertEqual(resource.sid, 1)
        self.assertEqual(resource.blah, 2)
        self.assertEqual(resource.__dict__, resource_args)

    def test_repr(self):
        resource_args = {'sid': 1}
        resource = Resource(**resource_args)
        self.assertEqual('Resource(sid=1)', '%r' % resource)

    def test_all(self):
        resource_args = {'name': [{'sid': 1}]}
        mock_client = mock.Mock()
        mock_response = mock.Mock()
        mock_response.json = resource_args
        mock_client.get.return_value = mock_response
        Resource.client = mock_client
        Resource._name = 'name'
        resources = Resource.all()
        self.assertTrue(isinstance(resources, list))
        self.assertTrue(isinstance(resources[0], Resource))
        self.assertEqual(resources[0].sid, 1)
        mock_client.get.assert_called_once_with('name')

    def test_find(self):
        pass

    def test_save_when_payment_has_no_id_issues_POST(self):
        pass

    def test_save_when_payment_has_no_sid_issues_POST(self):
        pass

    def test_save_when_payment_has_an_id_issues_PUT(self):
        pass

    def test_save_when_payment_has_an_sid_issues_PUT(self):
        pass

    def test_delete(self):
        pass

    def test_get_path(self):
        pass
