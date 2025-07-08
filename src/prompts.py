from typing import Literal

from src.utils import check

def get_sentence_example_prompt(word_or_phrase: str, language: Literal["German", "English"]) -> str:
    check(language in ["German", "English"], f"Unsupported language: {language}")
    return f'Generate one sentence in {language} with the use of the word or phrase "{word_or_phrase}".'
