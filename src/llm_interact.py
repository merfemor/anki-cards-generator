import logging

import ollama
from openai import OpenAI

from src.configuration import get_global_llm_provider, LLMProvider


def ask_llm(prompt: str) -> str:
    # TODO: how to set a random seed?
    llm_provider = get_global_llm_provider()
    logging.info(f"LLM request, provider={llm_provider.value}, prompt='{prompt}'")
    try:
        match llm_provider:
            case LLMProvider.OLLAMA:
                response_text = ask_ollama(prompt)
            case LLMProvider.OPENAI:
                response_text = ask_openai(prompt)
            case _:
                raise ValueError(f"Not handled branch for LLM provider: {llm_provider}")
    except Exception as e:
        raise Exception("Exception during LLM request") from e
    logging.info(f"LLM response='{response_text}'")
    return response_text


def ask_ollama(prompt: str) -> str:
    response = ollama.generate(model='llama3.1:8b', prompt=prompt, options={"top_k": 20})
    return response['response']


def ask_openai(prompt: str) -> str:
    openai_client = OpenAI()
    response = openai_client.responses.create(
        model="gpt-4.1-nano",
        input=prompt,
    )
    return response.output_text
