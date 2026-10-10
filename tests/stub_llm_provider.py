from typing import Final

from app.llm_interact import LlmProvider


STANDARD_RESPONSE_STUB: Final[str] = "This is just some stub sentence example."


class StubLlmProvider(LlmProvider):
    def __init__(self, response_text: str = STANDARD_RESPONSE_STUB):
        self.response_text = response_text

    async def ask_llm(self, prompt: str) -> str:
        return self.response_text
