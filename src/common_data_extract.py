from typing import Literal

from src.llm_interact import ask_llm
from src.prompts import get_sentence_example_prompt
from src.utils import check


async def generate_sentence_example_with_llm(word: str, language: Literal["English", "German"]) -> str:
    prompt = get_sentence_example_prompt(word, language)

    res = (await ask_llm(prompt)).strip()
    check(len(res) > len(word), f"Too short response: {res}")
    check(len(res) < 1000, f"Too long response, len={len(res)}")

    return res
