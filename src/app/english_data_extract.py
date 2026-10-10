import logging

from pydantic import BaseModel

from app.common_data_extract import generate_sentence_example_with_llm
from app.spelling import correct_spelling
from app.translate import translate_text
from app.utils import check
from app.word_hints import WordHints


class EnglishWordData(BaseModel):
    word: str
    translated_ru: str
    sentence_example: str
    sentence_example_translated_ru: str


async def prepare_data_for_english_word(word: str, hints: WordHints) -> EnglishWordData:
    check(len(word.strip()) > 0, "Expected non empty word")

    orig_word = word
    word = correct_spelling(word, language="en")
    if orig_word != word:
        logging.info(f"Corrected spelling from {orig_word} to {word}")

    en_sentence_example = await generate_sentence_example_with_llm(word, language="English", is_phrase=False)

    if hints.translated_ru:
        translated_ru = hints.translated_ru
    else:
        translated_ru = (await translate_text(word, src="en", dest="ru")).lower()

    return EnglishWordData(
        word=word,
        translated_ru=translated_ru,
        sentence_example=en_sentence_example,
        sentence_example_translated_ru=await translate_text(en_sentence_example, src="en", dest="ru"),
    )
