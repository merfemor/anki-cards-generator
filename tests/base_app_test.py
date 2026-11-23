from abc import ABC

from flask.ctx import RequestContext
from stub_llm_provider import STANDARD_RESPONSE_STUB, StubLlmProvider
from stub_translator import TRANSLATION_STUB, StubTranslator

from app.main import create_app
from app.tts import init_tts_engine


class AbstractAppRestTest(ABC):
    def setup_method(self) -> None:
        self.orig_app = create_app(
            StubLlmProvider(STANDARD_RESPONSE_STUB),
            StubTranslator(TRANSLATION_STUB),
            init_tts_engine(),
        )
        self.app = self.orig_app.test_client()
        self.orig_app.testing = True

    def get_test_context(self) -> RequestContext:
        return self.orig_app.test_request_context()
