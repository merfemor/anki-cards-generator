import argparse
import logging
from enum import Enum


class AIProvider(Enum):
    OLLAMA = "ollama"
    OPENAI = "openai"


AI_PROVIDER: AIProvider = AIProvider.OPENAI

def get_global_ai_provider() -> AIProvider:
    global AI_PROVIDER
    return AI_PROVIDER


def set_global_ai_provider(provider: str):
    global AI_PROVIDER
    logging.info(f"Using AI provider {provider}")
    match provider:
        case AIProvider.OLLAMA.value:
            AI_PROVIDER = AIProvider.OLLAMA
        case AIProvider.OPENAI.value:
            AI_PROVIDER = AIProvider.OPENAI
        case _:
            raise ValueError(f"Not handled branch for AI provider: {provider}")


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Run the Anki cards generator server')
    parser.add_argument('--ai-provider', choices=[AIProvider.OPENAI.value, AIProvider.OLLAMA.value],
                        default=AIProvider.OPENAI.value,
                        help='AI provider to use (default: openai)')
    return parser.parse_args()
