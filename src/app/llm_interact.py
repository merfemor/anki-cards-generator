import logging
import os
import sys
from abc import abstractmethod, ABC
from typing import Final, Callable

import ollama
import openai
from flask import current_app
from google import genai


async def ask_llm(prompt: str) -> str:
    llm_provider: LlmProvider = current_app.extensions["llm_provider"]
    try:
        response_text = await llm_provider.ask_llm(prompt)
    except Exception as e:
        raise Exception("Exception during LLM request") from e
    logging.debug(f"LLM response='{response_text}', prompt='{prompt}', provider={llm_provider.__class__.__name__}")
    return response_text


class LlmProvider(ABC):
    @abstractmethod
    async def ask_llm(self, prompt: str) -> str:
        pass


class OllamaLlmProvider(LlmProvider):
    OLLAMA_MODEL: Final[str] = "qwen3.5:4b"

    def __init__(self):
        self.early_check_ollama()

    async def ask_llm(self, prompt: str) -> str:
        client = ollama.AsyncClient()
        # Set top_k to have more conservative answers
        res = await client.generate(model=self.OLLAMA_MODEL, prompt=prompt, options={"top_k": 20}, think=False)
        response_text: str = res["response"]
        return response_text

    def early_check_ollama(self) -> None:
        try:
            available_models = ollama.list().models
        except ConnectionError:
            print("Error: Ollama is not accessible. Did you forget to start it?")
            sys.exit(1)

        available_model_names: list[str] = [m.model for m in available_models if m.model is not None]
        if self.OLLAMA_MODEL in available_model_names:
            logging.info(f"Ollama model {self.OLLAMA_MODEL} is available")
            return

        print(f"Error: model '{self.OLLAMA_MODEL}' is not found in Ollama.")
        if available_model_names:
            print(f"Available models: {', '.join(available_model_names)}")
        print(f"To install it execute: ollama pull '{self.OLLAMA_MODEL}'")
        sys.exit(1)


class OpenaiLlmProvider(LlmProvider):
    async def ask_llm(self, prompt: str) -> str:
        async with openai.AsyncOpenAI() as client:
            response = await client.responses.create(
                model="gpt-4.1-nano",
                input=prompt,
            )
            return response.output_text


class GeminiLlmProvider(LlmProvider):
    GEMINI_MODEL: Final[str] = "gemini-3.5-flash-lite"

    def __init__(self):
        api_key = os.environ.get("GEMINI_API_KEY")
        if api_key is None:
            print("Error: GEMINI_API_KEY env variable is not set.")
            sys.exit(1)
        self.api_key = api_key

    async def ask_llm(self, prompt: str) -> str:
        async with genai.Client(api_key=self.api_key).aio as client:
            response = await client.models.generate_content(
                model=self.GEMINI_MODEL,
                contents=prompt,
            )
            return response.text or ""


__LLM_PROVIDER_FACTORIES: Final[dict[str, Callable[[], LlmProvider]]] = {
    # Order is important, the first one will be the default option
    "ollama": OllamaLlmProvider,
    "openai": OpenaiLlmProvider,
    "gemini": GeminiLlmProvider,
}


def parse_llm_provider_argument() -> str:
    llm_providers = list(__LLM_PROVIDER_FACTORIES.keys())
    llm_provider_raw: str = os.getenv("LLM_PROVIDER", llm_providers[0])
    if llm_provider_raw not in llm_providers:
        print(f'Usage: invalid LLM_PROVIDER variable "{llm_provider_raw}". Choose from: {", ".join(llm_providers)}.')
        sys.exit(1)
    return llm_provider_raw


def init_llm_provider() -> LlmProvider:
    provider = parse_llm_provider_argument()
    logging.info(f"Using LLM provider {provider}")
    return __LLM_PROVIDER_FACTORIES[provider]()
