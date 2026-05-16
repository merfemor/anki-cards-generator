from typing import Literal

from app.llm_interact import ask_llm
from app.prompts import get_sentence_example_prompt
from app.utils import check


async def generate_sentence_example_with_llm(word: str, language: Literal["English", "German"], is_phrase: bool) -> str:
    prompt = get_sentence_example_prompt(word, language, is_phrase)

    res = (await ask_llm(prompt)).strip()
    check(len(res) > len(word), f"Too short response: {res}")
    check(len(res) < 1000, f"Too long response, len={len(res)}")

    return res
