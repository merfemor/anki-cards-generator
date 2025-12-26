from typing import Literal

from src.utils import check


def get_sentence_example_prompt(word_or_phrase: str, language: Literal["German", "English"], is_phrase: bool) -> str:
    check(language in ["German", "English"], f"Unsupported language: {language}")
    type = "phrase" if is_phrase else "word"
    return f'Generate one sentence in {language} using the {type} "{word_or_phrase}". The answer must only contain the sentence itself.'
