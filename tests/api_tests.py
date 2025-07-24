import json
import unittest

from main import app


class ApiEndpointsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def do_request(self, body: dict):
        return self.app.post("/api/generateCardsFile", data=json.dumps(body), content_type="application/json")

    def test_empty_words(self):
        response = self.do_request({"words": [], "language": "de"})
        self.assertEqual(response.status_code, 400)

    def test_absent_words(self):
        response = self.do_request({"language": "de"})
        self.assertEqual(response.status_code, 400)

    def test_absent_language(self):
        response = self.do_request({"words": ["Katze"]})
        self.assertEqual(response.status_code, 400)

    def test_not_supported_language(self):
        response = self.do_request({"words": ["katt"], "language": "sv"})
        self.assertEqual(response.status_code, 400)

    def test_home_page_ok_response(self):
        res = self.app.get("/")
        self.assertEqual(200, res.status_code)
