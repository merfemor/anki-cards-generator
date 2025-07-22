import unittest

from main import app


class ApiEndpointGenerateCardsFileTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_ok_response(self):
        res = self.app.get('/')
        self.assertEqual(200, res.status_code)
