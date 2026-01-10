from typing import Final

import pytest

from src.english_data_extract import EnglishWordData, prepare_data_for_english_word
from src.llm_interact import override_global_llm_provider_for_test
from src.translate import override_global_translator_for_test
from src.word_hints import WordHints
from stub_llm_provider import StubLlmProvider
from stub_translator import StubTranslator

sentence_example_stub_text: Final[str] = "." * 50
word_translated_stub: Final[str] = "_"
sentence_example_translated_ru_stub_text: Final[str] = word_translated_stub


@pytest.mark.asyncio(loop_scope="class")
class TestEnglishPrepareData:
    def setup_method(self) -> None:
        override_global_llm_provider_for_test(StubLlmProvider(sentence_example_stub_text))
        override_global_translator_for_test(StubTranslator(word_translated_stub))

    async def test_empty_word(self):
        with pytest.raises(ValueError):
            await self.prepare_data("")

    async def test_spaces(self):
        with pytest.raises(ValueError):
            await self.prepare_data("     ")

    async def test_noun(self):
        expected = EnglishWordData(
            original_word="cat",
            translated=word_translated_stub,
            sentence_example=sentence_example_stub_text,
            sentence_example_translated=sentence_example_translated_ru_stub_text,
        )
        assert expected == await self.prepare_data("cat")

    async def test_verb(self):
        expected = EnglishWordData(
            original_word="swim",
            translated=word_translated_stub,
            sentence_example=sentence_example_stub_text,
            sentence_example_translated=sentence_example_translated_ru_stub_text,
        )
        assert expected == await self.prepare_data("swim")

    async def test_verb_with_to(self):
        expected = EnglishWordData(
            original_word="to swim",
            translated=word_translated_stub,
            sentence_example=sentence_example_stub_text,
            sentence_example_translated=sentence_example_translated_ru_stub_text,
        )
        assert expected == await self.prepare_data("to swim")

    async def test_phrasal_verb(self):
        expected = EnglishWordData(
            original_word="cut off",
            translated=word_translated_stub,
            sentence_example=sentence_example_stub_text,
            sentence_example_translated=sentence_example_translated_ru_stub_text,
        )
        assert expected == await self.prepare_data("cut off")

    async def test_phrasal_verb_with_to(self):
        expected = EnglishWordData(
            original_word="to cut off",
            translated=word_translated_stub,
            sentence_example=sentence_example_stub_text,
            sentence_example_translated=sentence_example_translated_ru_stub_text,
        )
        assert expected == await self.prepare_data("to cut off")

    async def test_with_hint(self):
        expected = EnglishWordData(
            original_word="miscellaneous",
            translated="смешанный, разнообразный",
            sentence_example=sentence_example_stub_text,
            sentence_example_translated=sentence_example_translated_ru_stub_text,
        )
        assert expected == await prepare_data_for_english_word("miscellaneous", WordHints("смешанный, разнообразный"))

    async def test_word_with_mistake(self):
        actual = await self.prepare_data("heigh")
        assert actual.original_word == "high"

    async def test_phrase_with_mistake_not_corrected(self):
        actual = await self.prepare_data("make and efort")
        assert actual.original_word == "make and efort"

    async def prepare_data(self, word: str) -> EnglishWordData:
        return await prepare_data_for_english_word(word, hints=WordHints(""))
