import logging
import sys
from abc import abstractmethod, ABC
from typing import Final, Callable

import ollama
import openai


async def ask_llm(prompt: str) -> str:
    llm_provider = __LLM_PROVIDER
    logging.info(f"LLM request, provider={llm_provider.__class__.__name__}, prompt='{prompt}'")
    try:
        response_text = await llm_provider.ask_llm(prompt)
    except Exception as e:
        raise Exception("Exception during LLM request") from e
    logging.info(f"LLM response='{response_text}'")
    return response_text


class LlmProvider(ABC):
    @abstractmethod
    async def ask_llm(self, prompt: str) -> str:
        pass


class OllamaLlmProvider(LlmProvider):
    def __init__(self):
        self.early_check_ollama()

    async def ask_llm(self, prompt: str) -> str:
        client = ollama.AsyncClient()
        # Set top_k to have more conservative answers
        res = await client.generate(model="llama3.1:8b", prompt=prompt, options={"top_k": 20})
        response_text: str = res["response"]
        return response_text

    @staticmethod
    def early_check_ollama() -> None:
        try:
            ollama.list()
        except ConnectionError:
            print("Error: Ollama is not accessible. Did you forget to start it?")
            sys.exit(1)


class OpenaiLlmProvider(LlmProvider):
    def __init__(self):
        self.client = openai.AsyncOpenAI()

    async def ask_llm(self, prompt: str) -> str:
        response = await self.client.responses.create(
            model="gpt-4.1-nano",
            input=prompt,
        )
        return response.output_text


__LLM_PROVIDER_FACTORIES: Final[dict[str, Callable[[], LlmProvider]]] = {
    # Order is important, the first one will be the default option
    "ollama": OllamaLlmProvider,
    "openai": OpenaiLlmProvider,
}

__LLM_PROVIDER: LlmProvider


def llm_provider_choices() -> list[str]:
    return list(__LLM_PROVIDER_FACTORIES.keys())


def set_global_llm_provider(provider: str) -> None:
    global __LLM_PROVIDER
    logging.info(f"Using LLM provider {provider}")
    factory = __LLM_PROVIDER_FACTORIES[provider]
    __LLM_PROVIDER = factory()


def override_global_llm_provider_for_test(llm_provider: LlmProvider) -> None:
    global __LLM_PROVIDER
    __LLM_PROVIDER = llm_provider
