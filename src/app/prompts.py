from typing import Literal

from app.utils import check

PROMPT_TEMPLATE = """
Generate one sentence in {LANGUAGE} using the {TYPE} "{WORD_OR_PHRASE}". Output only the sentence and nothing else (no quotation marks, no notes, etc.) Do not use markdown, formatting, or styling. Max response length is {MAX_LENGTH} characters.
""".strip()


def get_sentence_example_prompt(
    word_or_phrase: str, language: Literal["German", "English"], is_phrase: bool, max_length: int
) -> str:
    check(language in ["German", "English"], f"Unsupported language: {language}")
    _type = "phrase" if is_phrase else "word"
    return PROMPT_TEMPLATE.format(LANGUAGE=language, TYPE=_type, WORD_OR_PHRASE=word_or_phrase, MAX_LENGTH=max_length)
