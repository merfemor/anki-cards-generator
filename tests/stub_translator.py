from src.translate import Translator


class StubTranslator(Translator):
    def __init__(self, response: str):
        self.response = response

    async def translate_text(self, text: str, src: str, dest: str) -> str:
        return self.response
