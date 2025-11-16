import pytest

from src.german_data_extract import GermanWordData, PartOfSpeech, prepare_data_for_german_word
from src.llm_interact import override_global_llm_provider_for_test
from src.translate import override_global_translator_for_test
from src.word_hints import WordHints
from stub_llm_provider import StubLlmProvider
from stub_translator import StubTranslator


@pytest.mark.asyncio(loop_scope="class")
class TestGermanPhrasePrepareData:
    def setup_method(self) -> None:
        override_global_llm_provider_for_test(StubLlmProvider("." * 50))
        override_global_translator_for_test(StubTranslator("_"))

    async def test_collocation(self):
        actual = await self.prepare_data("eine Entscheidung treffen")
        assert actual.pos_tag == ""
        assert actual.part_of_speech == PartOfSpeech.Other
        assert actual.word_infinitive == "eine Entscheidung treffen"
        assert actual.word_note_suffix == ""
        assert actual.noun_properties is None

    async def test_phrase_with_grammatical_case_note(self):
        actual = await self.prepare_data("Angst haben vor (+Dat)")
        assert actual.pos_tag == ""
        assert actual.part_of_speech == PartOfSpeech.Other
        assert actual.word_infinitive == "Angst haben vor"
        assert actual.word_note_suffix == "(+Dat)"
        assert actual.noun_properties is None

    @staticmethod
    async def prepare_data(phrase: str) -> GermanWordData:
        return await prepare_data_for_german_word(phrase, hints=WordHints(""))
