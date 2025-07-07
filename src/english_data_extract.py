from dataclasses import dataclass

from src.llm_interact import ask_llm
from src.translate import translate_text
from src.utils import check


@dataclass
class EnglishWordData:
    original_word: str
    translated: str
    sentence_example: str
    sentence_example_translated: str


def prepare_data_for_english_word(word: str) -> EnglishWordData:
    en_sentence_example = get_english_sentence_example(word)
    return EnglishWordData(
        original_word=word,
        translated=translate_text(word, src="en", dest="ru").lower(),
        sentence_example=en_sentence_example,
        sentence_example_translated=translate_text(en_sentence_example, src="en", dest="ru")
    )


def get_english_sentence_example(word: str) -> str:
    prompt = f"Generate one simple sentence in English with the use of the word \"{word}\""

    res = ask_llm(prompt).strip()
    check(len(res) > len(word), f"Too short response: {res}")
    check(len(res) < 1000, f"Too long response, len={len(res)}")

    return res
