import pytest

from app.german_data_extract import GermanWordData, PartOfSpeech, prepare_data_for_german_word
from app.word_hints import WordHints
from base_app_test import AbstractAppRestTest


@pytest.mark.asyncio(loop_scope="class")
class TestGermanPhrasePrepareData(AbstractAppRestTest):
    async def test_collocation(self):
        actual = await self.prepare_data("eine Entscheidung treffen")
        assert actual.pos_tag == ""
        assert actual.part_of_speech == PartOfSpeech.Other
        assert actual.raw_word == "eine Entscheidung treffen"
        assert actual.word == "eine Entscheidung treffen"
        assert actual.word_note_suffix == ""
        assert actual.noun_properties is None

    async def test_phrase_with_grammatical_case_note(self):
        actual = await self.prepare_data("Angst haben vor (+Dat)")
        assert actual.pos_tag == ""
        assert actual.part_of_speech == PartOfSpeech.Other
        assert actual.raw_word == "Angst haben vor (+Dat)"
        assert actual.word == "Angst haben vor"
        assert actual.word_note_suffix == "(+Dat)"
        assert actual.noun_properties is None

    async def test_phrase_with_mistake_given_not_corrected(self):
        actual = await self.prepare_data("Entsheidung treffen")
        assert actual.raw_word == "Entsheidung treffen"
        assert actual.word == "Entsheidung treffen"

    async def prepare_data(self, phrase: str) -> GermanWordData:
        with self.get_test_context():
            return await prepare_data_for_german_word(phrase, hints=WordHints(""))
