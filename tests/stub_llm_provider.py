from llm_interact import LlmProvider


class StubLlmProvider(LlmProvider):
    def __init__(self, response_test: str):
        self.response_test = response_test

    async def ask_llm(self, _: str) -> str:
        return self.response_test
