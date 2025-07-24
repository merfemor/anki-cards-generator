import json

from main import app


class TestApiEndpoints:
    def setup_method(self):
        self.app = app.test_client()
        self.app.testing = True

    def do_request(self, body: dict):
        return self.app.post("/api/generateCardsFile", data=json.dumps(body), content_type="application/json")

    def test_empty_words(self):
        response = self.do_request({"words": [], "language": "de"})
        assert response.status_code == 400

    def test_absent_words(self):
        response = self.do_request({"language": "de"})
        assert response.status_code == 400

    def test_absent_language(self):
        response = self.do_request({"words": ["Katze"]})
        assert response.status_code == 400

    def test_not_supported_language(self):
        response = self.do_request({"words": ["katt"], "language": "sv"})
        assert response.status_code == 400

    def test_home_page_ok_response(self):
        res = self.app.get("/")
        assert res.status_code == 200
