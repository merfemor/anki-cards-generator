import argparse
import logging
from enum import Enum


class LLMProvider(Enum):
    OLLAMA = "ollama"
    OPENAI = "openai"


__LLM_PROVIDER: LLMProvider = LLMProvider.OPENAI

def get_global_llm_provider() -> LLMProvider:
    return __LLM_PROVIDER


def set_global_llm_provider(provider: str) -> None:
    global __LLM_PROVIDER
    logging.info(f"Using LLM provider {provider}")
    match provider:
        case LLMProvider.OLLAMA.value:
            __LLM_PROVIDER = LLMProvider.OLLAMA
        case LLMProvider.OPENAI.value:
            __LLM_PROVIDER = LLMProvider.OPENAI
        case _:
            raise ValueError(f"Not handled branch for LLM provider: {provider}")


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Run the Anki cards generator server')
    parser.add_argument('--llm-provider', choices=[LLMProvider.OPENAI.value, LLMProvider.OLLAMA.value],
                        default=LLMProvider.OPENAI.value,
                        help='LLM provider to use (default: openai)')
    return parser.parse_args()
