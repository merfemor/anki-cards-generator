import asyncio
import logging
import os
import sys
from typing import Callable

import ollama
from openai import OpenAI

from src.configuration import get_global_llm_provider, LLMProvider


async def ask_llm(prompt: str) -> str:
    # TODO: how to set a random seed?
    llm_provider = get_global_llm_provider()
    logging.info(f"LLM request, provider={llm_provider.value}, prompt='{prompt}'")
    try:
        match llm_provider:
            case LLMProvider.OLLAMA:
                response_text = await ask_ollama(prompt)
            case LLMProvider.OPENAI:
                response_text = ask_openai(prompt)
            case _:
                raise ValueError(f"Not handled branch for LLM provider: {llm_provider}")
    except Exception as e:
        raise Exception("Exception during LLM request") from e
    logging.info(f"LLM response='{response_text}'")
    return response_text


async def ask_ollama(prompt: str) -> str:
    def blocking() -> str:
        response_text: str = ollama.generate(model='llama3.1:8b', prompt=prompt, options={"top_k": 20})['response']
        return response_text

    return await wrap_blocking_into_async(blocking)


# Trick to run existing blocking code from a coroutine
async def wrap_blocking_into_async[R](fn: Callable[[], R]) -> R:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, fn)


def ask_openai(prompt: str) -> str:
    openai_client = OpenAI()
    response = openai_client.responses.create(
        model="gpt-4.1-nano",
        input=prompt,
    )
    return response.output_text

def early_check_llm_environment() -> None:
    provider = get_global_llm_provider()
    match provider:
        case LLMProvider.OLLAMA:
            early_check_ollama()
        case LLMProvider.OPENAI:
            early_check_openai()
        case _:
            raise ValueError(f"Not handled branch for LLM provider: {provider}")


def early_check_ollama() -> None:
    try:
        ollama.list()
    except ConnectionError:
        print("Error: Ollama is not accessible. Did you forget to start it?")
        sys.exit(1)


def early_check_openai() -> None:
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        print("Error: OPENAI_API_KEY environment variable is not set.")
        sys.exit(1)
