import json
from typing import Final

from app.llm_interact import override_global_llm_provider_for_test
from app.main import app
from app.tts import init_tts_engine
from app.translate import override_global_translator_for_test
from stub_llm_provider import StubLlmProvider
from stub_translator import StubTranslator

SENTENCE_EXAMPLE_STUB: Final[str] = "." * 50
TRANSLATION_STUB: Final[str] = "_"


class TestApiEndpoints:
    def setup_method(self) -> None:
        override_global_llm_provider_for_test(StubLlmProvider(SENTENCE_EXAMPLE_STUB))
        override_global_translator_for_test(StubTranslator(TRANSLATION_STUB))
        init_tts_engine()
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

    def test_generate_german_deck_ok_response(self) -> None:
        response = self.do_request({"words": [{"word": "Katze"}], "language": "de"})
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/octet-stream"

    def test_home_page_ok_response(self):
        res = self.app.get("/")
        assert res.status_code == 200
