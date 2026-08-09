import textwrap
from typing import Literal, Final

from app.llm_interact import ask_llm
from app.prompts import get_sentence_example_prompt
from app.utils import check

MAX_RESPONSE_LENGTH: Final[int] = 1000


async def generate_sentence_example_with_llm(word: str, language: Literal["English", "German"], is_phrase: bool) -> str:
    prompt = get_sentence_example_prompt(word, language, is_phrase, MAX_RESPONSE_LENGTH)

    res = (await ask_llm(prompt)).strip()
    check(len(res) > len(word), f"Too short response: {res}")
    shortened = textwrap.shorten(res, width=120, placeholder="...")
    check(len(res) < MAX_RESPONSE_LENGTH, f"Too long response, len={len(res)}: {shortened}")

    return res
