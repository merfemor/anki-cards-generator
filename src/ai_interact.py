import logging

import ollama
from openai import OpenAI

from src.configuration import get_global_ai_provider, AIProvider


def ask_ai(prompt: str) -> str:
    # TODO: how to set a random seed?
    ai_provider = get_global_ai_provider()
    logging.info(f"AI request={prompt} on {ai_provider.value}")
    try:
        match ai_provider:
            case AIProvider.OLLAMA:
                response_text = ask_ai_ollama(prompt)
            case AIProvider.OPENAI:
                response_text = ask_ai_openai(prompt)
            case _:
                raise ValueError(f"Not handled branch for AI provider: {ai_provider}")
    except Exception as e:
        raise Exception("Exception during AI request") from e
    logging.info(f"AI response={response_text}")
    return response_text


def ask_ai_ollama(prompt: str) -> str:
    response = ollama.generate(model='llama3.1:8b', prompt=prompt, options={"top_k": 20})
    return response['response']


def ask_ai_openai(prompt: str) -> str:
    openai_client = OpenAI()
    response = openai_client.responses.create(
        model="gpt-4.1-nano",
        input=prompt,
    )
    return response.output_text
