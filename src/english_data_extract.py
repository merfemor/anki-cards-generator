from dataclasses import dataclass

from src.common_data_extract import generate_sentence_example_with_llm
from src.translate import translate_text
from src.utils import check
from src.word_hints import WordHints


@dataclass
class EnglishWordData:
    original_word: str
    translated: str
    sentence_example: str
    sentence_example_translated: str


async def prepare_data_for_english_word(word: str, hints: WordHints, stub_llm: bool = False) -> EnglishWordData:
    check(len(word.strip()) > 0, "Expected non empty word")

    if stub_llm:
        en_sentence_example = ""
    else:
        en_sentence_example = await generate_sentence_example_with_llm(word, language="English")

    if hints.translated_ru:
        translated = hints.translated_ru
    else:
        translated = (await translate_text(word, src="en", dest="ru")).lower()

    return EnglishWordData(
        original_word=word,
        translated=translated,
        sentence_example=en_sentence_example,
        sentence_example_translated=await translate_text(en_sentence_example, src="en", dest="ru"),
    )
