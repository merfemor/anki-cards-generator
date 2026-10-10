from typing import Any, Final

from flask import Response

from app.llm_interact import override_global_llm_provider_for_test
from app.main import app
from app.tts import init_tts_engine
from app.translate import override_global_translator_for_test
from stub_llm_provider import StubLlmProvider
from stub_translator import StubTranslator

SENTENCE_EXAMPLE_STUB: Final[str] = "." * 50
TRANSLATION_STUB: Final[str] = "_"
GENERATE_WORD_DATA_ENDPOINT: Final[str] = "/api/generateWordData"
EXPORT_DECK_FILE_ENDPOINT: Final[str] = "/api/exportDeckFile"


class EndpointTestBase:
    endpoint: str

    def setup_method(self) -> None:
        override_global_llm_provider_for_test(StubLlmProvider(SENTENCE_EXAMPLE_STUB))
        override_global_translator_for_test(StubTranslator(TRANSLATION_STUB))
        init_tts_engine()
        self.app = app.test_client()
        self.app.testing = True

    def do_request(self, body: Any) -> Response:
        return self.app.post(self.endpoint, json=body)

    def test_absent_language(self):
        assert self.do_request({"word": "Katze"}).status_code == 400

    def test_not_supported_language(self):
        assert self.do_request({"word": "katt", "language": "sv"}).status_code == 400

    def test_malformed_json_body(self):
        response = self.app.post(self.endpoint, data="{not json", content_type="application/json")
        assert response.status_code == 400


class TestGenerateWordDataEndpoint(EndpointTestBase):
    endpoint = GENERATE_WORD_DATA_ENDPOINT

    def test_absent_word(self):
        assert self.do_request({"language": "de"}).status_code == 400

    def test_blank_word(self):
        assert self.do_request({"word": "   ", "language": "de"}).status_code == 400

    def test_word_of_wrong_type(self):
        assert self.do_request({"word": 42, "language": "de"}).status_code == 400

    def test_hints_of_wrong_type(self):
        assert self.do_request({"word": "Katze", "hints": "cat", "language": "de"}).status_code == 400

    def test_german_word_data_ok_response(self):
        word_data = self.extract_word_data("Katze", "de")
        assert word_data["word"] == "Katze"
        assert word_data["translated_ru"] == TRANSLATION_STUB
        assert word_data["sentence_example"] == SENTENCE_EXAMPLE_STUB

    def test_english_word_data_ok_response(self):
        word_data = self.extract_word_data("cat", "en")
        assert word_data["word"] == "cat"
        assert word_data["translated_ru"] == TRANSLATION_STUB
        assert word_data["sentence_example"] == SENTENCE_EXAMPLE_STUB

    def extract_word_data(self, word: str, language: str) -> dict[str, Any]:
        response = self.do_request({"word": word, "language": language})
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"
        return response.get_json()


class TestExportDeckFileEndpoint(EndpointTestBase):
    endpoint = EXPORT_DECK_FILE_ENDPOINT

    def test_absent_language(self):
        assert self.do_request({"words": [{"word": "Katze"}]}).status_code == 400

    def test_not_supported_language(self):
        assert self.do_request({"words": [{"word": "katt"}], "language": "sv"}).status_code == 400

    def test_empty_words(self):
        assert self.do_request({"words": [], "language": "de"}).status_code == 400

    def test_absent_words(self):
        assert self.do_request({"language": "de"}).status_code == 400

    def test_word_data_of_wrong_type(self):
        assert self.do_request({"words": ["Katze"], "language": "de"}).status_code == 400

    def test_incomplete_word_data(self):
        assert self.do_request({"words": [{"word": "Katze"}], "language": "de"}).status_code == 400

    def test_german_deck_file_ok_response(self):
        self.assert_deck_file_generated("Katze", "de")

    def test_english_deck_file_ok_response(self):
        self.assert_deck_file_generated("cat", "en")

    def assert_deck_file_generated(self, word: str, language: str) -> None:
        response = self.app.post(GENERATE_WORD_DATA_ENDPOINT, json={"word": word, "language": language})
        assert response.status_code == 200
        word_data = response.get_json()

        response = self.do_request({"words": [word_data], "language": language})

        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/octet-stream"
        assert len(response.data) > 0


class TestHomePage:
    def test_home_page_ok_response(self):
        assert app.test_client().get("/").status_code == 200
