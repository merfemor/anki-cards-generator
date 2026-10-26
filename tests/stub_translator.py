from typing import Final

from app.translate import Translator

TRANSLATION_STUB: Final[str] = "_"


class StubTranslator(Translator):
    def __init__(self, response: str):
        self.response = response

    async def translate_text(self, text: str, src: str, dest: str) -> str:
        return self.response
