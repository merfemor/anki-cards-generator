from dataclasses import dataclass

from src.common_data_extract import generate_sentence_example_with_llm
from src.translate import translate_text


@dataclass
class EnglishWordData:
    original_word: str
    translated: str
    sentence_example: str
    sentence_example_translated: str


def prepare_data_for_english_word(word: str) -> EnglishWordData:
    en_sentence_example = generate_sentence_example_with_llm(word, language="English")
    return EnglishWordData(
        original_word=word,
        translated=translate_text(word, src="en", dest="ru").lower(),
        sentence_example=en_sentence_example,
        sentence_example_translated=translate_text(en_sentence_example, src="en", dest="ru")
    )
