import random
from typing import Final

import pytest

import src.german_data_extract
import src.utils
from src.anki_common import get_audio_file_name_for_phrase, get_audio_file_name_for_sentence
from src.english_data_extract import prepare_data_for_english_word, EnglishWordData
from src.german_anki_generate import shorten_german_noun_plural_form_for_anki_card
from src.german_data_extract import GermanWordData, PartOfSpeech
from src.llm_interact import override_global_llm_provider_for_test
from src.translate import override_global_translator_for_test
from src.word_hints import WordHints
from stub_llm_provider import StubLlmProvider
from stub_translator import StubTranslator

sentence_example_stub_text: Final[str] = "." * 50
word_translated_stub: Final[str] = "_"
sentence_example_translated_en_stub_text: Final[str] = word_translated_stub
sentence_example_translated_ru_stub_text: Final[str] = word_translated_stub


@pytest.mark.asyncio(loop_scope="class")
class TestGermanPrepareData:
    def setup_method(self) -> None:
        override_global_llm_provider_for_test(StubLlmProvider(sentence_example_stub_text))
        override_global_translator_for_test(StubTranslator(word_translated_stub))

    async def test_empty_string(self):
        with pytest.raises(ValueError):
            await self.prepare_data("")

    async def test_spaces_string(self):
        with pytest.raises(ValueError):
            await self.prepare_data("   ")

    async def test_non_words_symbol(self):
        with pytest.raises(ValueError):
            await self.prepare_data("$")

    async def test_non_words_dot(self):
        with pytest.raises(ValueError):
            await self.prepare_data(".")

    async def test_non_words_comma(self):
        with pytest.raises(ValueError):
            await self.prepare_data(",")

    async def test_non_words_dash(self):
        with pytest.raises(ValueError):
            await self.prepare_data("-")

    async def test_noun_feminine(self):
        expected = GermanWordData(
            word_infinitive="Katze",
            pos_tag="NN",
            part_of_speech=PartOfSpeech.Noun,
            translated_en=word_translated_stub,
            translated_ru=word_translated_stub,
            noun_properties=src.german_data_extract.GermanNounProperties(
                singular_form="Katze", plural_form="Katzen", genus="f", article="die"
            ),
            sentence_example=sentence_example_stub_text,
            sentence_example_translated_en=sentence_example_translated_en_stub_text,
        )
        assert expected == await self.prepare_data("Katze")

    async def test_noun_no_plural(self):
        expected = GermanWordData(
            word_infinitive="Schnee",
            pos_tag="NN",
            part_of_speech=PartOfSpeech.Noun,
            translated_en=word_translated_stub,
            translated_ru=word_translated_stub,
            noun_properties=src.german_data_extract.GermanNounProperties(
                singular_form="Schnee", plural_form="", genus="m", article="der"
            ),
            sentence_example=sentence_example_stub_text,
            sentence_example_translated_en=sentence_example_translated_en_stub_text,
        )
        assert expected == await self.prepare_data("Schnee")

    async def test_noun_two_plural(self):
        expected = GermanWordData(
            word_infinitive="Band",
            pos_tag="NN",
            part_of_speech=PartOfSpeech.Noun,
            translated_en=word_translated_stub,
            translated_ru=word_translated_stub,
            noun_properties=src.german_data_extract.GermanNounProperties(
                singular_form="Band", plural_form="Bänder", genus="n", article="das"
            ),
            sentence_example=sentence_example_stub_text,
            sentence_example_translated_en=sentence_example_translated_en_stub_text,
        )
        assert expected == await self.prepare_data("Band")

    async def test_noun_no_singular(self):
        expected = GermanWordData(
            word_infinitive="Ferien",
            pos_tag="NN",
            part_of_speech=PartOfSpeech.Noun,
            translated_en=word_translated_stub,
            translated_ru=word_translated_stub,
            noun_properties=src.german_data_extract.GermanNounProperties(
                singular_form="", plural_form="Ferien", genus="pl", article="die"
            ),
            sentence_example=sentence_example_stub_text,
            sentence_example_translated_en=sentence_example_translated_en_stub_text,
        )
        assert expected == await self.prepare_data("Ferien")

    async def test_noun_ambiguity_with_verb(self):
        expected = GermanWordData(
            word_infinitive="Schwimmen",
            pos_tag="NNI",
            part_of_speech=PartOfSpeech.Noun,
            translated_en=word_translated_stub,
            translated_ru=word_translated_stub,
            noun_properties=src.german_data_extract.GermanNounProperties(
                singular_form="Schwimmen", plural_form="", genus="n", article="das"
            ),
            sentence_example=sentence_example_stub_text,
            sentence_example_translated_en=sentence_example_translated_en_stub_text,
        )
        assert expected == await self.prepare_data("Schwimmen")

    async def test_verb(self):
        expected = GermanWordData(
            word_infinitive="schlafen",
            pos_tag="VV(INF)",
            part_of_speech=PartOfSpeech.Verb,
            translated_en="to " + word_translated_stub,
            translated_ru=word_translated_stub,
            noun_properties=None,
            sentence_example=sentence_example_stub_text,
            sentence_example_translated_en=sentence_example_translated_en_stub_text,
        )
        assert expected == await self.prepare_data("schlafen")

    async def test_adjective(self):
        expected = GermanWordData(
            word_infinitive="lustig",
            pos_tag="ADJ(D)",
            part_of_speech=PartOfSpeech.Other,
            translated_en=word_translated_stub,
            translated_ru=word_translated_stub,
            noun_properties=None,
            sentence_example=sentence_example_stub_text,
            sentence_example_translated_en=sentence_example_translated_en_stub_text,
        )
        assert expected == await self.prepare_data("lustig")

    async def test_subordinating_conjunction(self):
        expected = GermanWordData(
            word_infinitive="obgleich",
            pos_tag="KOUS",
            part_of_speech=PartOfSpeech.Other,
            translated_en=word_translated_stub,
            translated_ru=word_translated_stub,
            noun_properties=None,
            sentence_example=sentence_example_stub_text,
            sentence_example_translated_en=sentence_example_translated_en_stub_text,
        )
        assert expected == await self.prepare_data("obgleich")

    async def test_coordinating_conjunction(self):
        expected = GermanWordData(
            word_infinitive="und",
            pos_tag="KON",
            part_of_speech=PartOfSpeech.Other,
            translated_en=word_translated_stub,
            translated_ru=word_translated_stub,
            noun_properties=None,
            sentence_example=sentence_example_stub_text,
            sentence_example_translated_en=sentence_example_translated_en_stub_text,
        )
        assert expected == await self.prepare_data("und")

    async def test_adverb(self):
        expected = GermanWordData(
            word_infinitive="gerade",
            pos_tag="ADV",
            part_of_speech=PartOfSpeech.Other,
            translated_en=word_translated_stub,
            translated_ru=word_translated_stub,
            noun_properties=None,
            sentence_example=sentence_example_stub_text,
            sentence_example_translated_en=sentence_example_translated_en_stub_text,
        )
        assert expected == await self.prepare_data("gerade")

    async def test_with_hint(self):
        expected = GermanWordData(
            word_infinitive="lustig",
            pos_tag="ADJ(D)",
            part_of_speech=PartOfSpeech.Other,
            translated_en=word_translated_stub,
            translated_ru="смешной, весёлый",
            noun_properties=None,
            sentence_example=sentence_example_stub_text,
            sentence_example_translated_en=sentence_example_translated_en_stub_text,
        )
        assert expected == await src.german_data_extract.prepare_data_for_german_word(
            "lustig",
            hints=WordHints("смешной, весёлый"),
        )

    async def test_preposition(self):
        expected = GermanWordData(
            word_infinitive="durch",
            pos_tag="APPR",
            part_of_speech=PartOfSpeech.Other,
            translated_en=word_translated_stub,
            translated_ru=word_translated_stub,
            noun_properties=None,
            sentence_example=sentence_example_stub_text,
            sentence_example_translated_en=sentence_example_translated_en_stub_text,
        )
        assert expected == await self.prepare_data("durch")

    async def test_collocation(self):
        expected = GermanWordData(
            word_infinitive="eine Entscheidung treffen",
            pos_tag="",
            part_of_speech=PartOfSpeech.Other,
            translated_en=word_translated_stub,
            translated_ru=word_translated_stub,
            noun_properties=None,
            sentence_example=sentence_example_stub_text,
            sentence_example_translated_en=sentence_example_translated_en_stub_text,
        )
        assert expected == await self.prepare_data("eine Entscheidung treffen")

    async def test_rare_compound_word(self):
        with pytest.raises(NotImplementedError):
            await self.prepare_data("Kuddelmuddelkiste")

    async def test_noun_with_article_given(self):
        expected = GermanWordData(
            word_infinitive="Katze",
            pos_tag="NN",
            part_of_speech=PartOfSpeech.Noun,
            translated_en=word_translated_stub,
            translated_ru=word_translated_stub,
            noun_properties=src.german_data_extract.GermanNounProperties(
                singular_form="Katze", plural_form="Katzen", genus="f", article="die"
            ),
            sentence_example=sentence_example_stub_text,
            sentence_example_translated_en=sentence_example_translated_en_stub_text,
        )
        assert expected == await self.prepare_data("die Katze")

    async def test_noun_in_plural_given(self):
        expected = GermanWordData(
            word_infinitive="Markt",
            pos_tag="NN",
            part_of_speech=PartOfSpeech.Noun,
            translated_en=word_translated_stub,
            translated_ru=word_translated_stub,
            noun_properties=src.german_data_extract.GermanNounProperties(
                singular_form="Markt", plural_form="Märkte", genus="m", article="der"
            ),
            sentence_example=sentence_example_stub_text,
            sentence_example_translated_en=sentence_example_translated_en_stub_text,
        )
        assert expected == await self.prepare_data("Märkte")

    async def test_adjective_conjugated_given(self):
        expected = GermanWordData(
            word_infinitive="schnell",
            pos_tag="ADJ(A)",
            part_of_speech=PartOfSpeech.Other,
            translated_en=word_translated_stub,
            translated_ru=word_translated_stub,
            noun_properties=None,
            sentence_example=sentence_example_stub_text,
            sentence_example_translated_en=sentence_example_translated_en_stub_text,
        )
        assert expected == await self.prepare_data("schnelle")

    async def test_noun_with_mistake_given(self):
        with pytest.raises(NotImplementedError):
            await self.prepare_data("Erfarung")

    async def test_verb_with_mistake_given(self):
        expected = GermanWordData(
            word_infinitive="empfeln",
            pos_tag="VV(INF)",
            part_of_speech=PartOfSpeech.Verb,
            translated_en="to " + word_translated_stub,
            translated_ru=word_translated_stub,
            noun_properties=None,
            sentence_example=sentence_example_stub_text,
            sentence_example_translated_en=sentence_example_translated_en_stub_text,
        )
        assert expected == await self.prepare_data("empfelen")

    async def test_reflexive_verb(self):
        expected = GermanWordData(
            word_infinitive="sich interessieren",
            pos_tag="VV(PP)",
            part_of_speech=PartOfSpeech.Verb,
            translated_en="to " + word_translated_stub,
            translated_ru=word_translated_stub,
            noun_properties=None,
            sentence_example=sentence_example_stub_text,
            sentence_example_translated_en=sentence_example_translated_en_stub_text,
        )
        assert expected == await self.prepare_data("sich interessieren")

    async def test_rare_adjective(self):
        # Identified as FM = Fremdsprachliches Material
        expected = GermanWordData(
            word_infinitive="perplex",
            pos_tag="FM",
            part_of_speech=PartOfSpeech.Other,
            translated_en=word_translated_stub,
            translated_ru=word_translated_stub,
            noun_properties=None,
            sentence_example=sentence_example_stub_text,
            sentence_example_translated_en=sentence_example_translated_en_stub_text,
        )
        assert expected == await self.prepare_data("perplex")

    async def test_adjective_detected_as_noun_not_found_in_dict(self):
        expected = GermanWordData(
            word_infinitive="zwanglos",
            pos_tag="NN",
            part_of_speech=PartOfSpeech.Other,
            translated_en=word_translated_stub,
            translated_ru=word_translated_stub,
            noun_properties=None,
            sentence_example=sentence_example_stub_text,
            sentence_example_translated_en=sentence_example_translated_en_stub_text,
        )
        assert expected == await self.prepare_data("zwanglos")

    async def test_reflexive_verb_with_sich_specified(self):
        expected = GermanWordData(
            word_infinitive="sich vorstellen",
            pos_tag="VV(INF)",
            part_of_speech=PartOfSpeech.Verb,
            translated_en="to " + word_translated_stub,
            translated_ru=word_translated_stub,
            noun_properties=None,
            sentence_example=sentence_example_stub_text,
            sentence_example_translated_en=sentence_example_translated_en_stub_text,
        )
        assert expected == await self.prepare_data("sich vorstellen")

    async def test_reflexive_verb_with_sich_specified_2(self):
        expected = GermanWordData(
            word_infinitive="sich schämen",
            pos_tag="VV(INF)",
            part_of_speech=PartOfSpeech.Verb,
            translated_en="to " + word_translated_stub,
            translated_ru=word_translated_stub,
            noun_properties=None,
            sentence_example=sentence_example_stub_text,
            sentence_example_translated_en=sentence_example_translated_en_stub_text,
        )
        assert expected == await self.prepare_data("sich schämen")

    async def test_verb_false_positively_detected_as_adjective(self):
        actual = await self.prepare_data("lauten")
        assert actual.pos_tag == "ADJ(A)"
        assert actual.part_of_speech == PartOfSpeech.Other
        assert actual.word_infinitive == "laut"
        assert actual.noun_properties is None

    async def test_adjective_false_positively_detected_as_verb(self):
        actual = await self.prepare_data("bewusst")
        assert actual.pos_tag == "VV(PP)"
        assert actual.part_of_speech == PartOfSpeech.Verb
        assert actual.word_infinitive == "bewussen"
        assert actual.noun_properties is None

    async def test_verb_with_grammatical_case_note(self):
        actual = await self.prepare_data("anrufen (+Akk)")
        assert actual.pos_tag == "VV(INF)"
        assert actual.part_of_speech == PartOfSpeech.Verb
        assert actual.word_infinitive == "anrufen"
        assert actual.word_note_suffix == "(+Akk)"
        assert actual.noun_properties is None

    async def test_phrase_with_grammatical_case_note(self):
        actual = await self.prepare_data("Angst haben vor (+Dat)")
        assert actual.pos_tag == ""
        assert actual.part_of_speech == PartOfSpeech.Other
        assert actual.word_infinitive == "Angst haben vor"
        assert actual.word_note_suffix == "(+Dat)"
        assert actual.noun_properties is None

    async def prepare_data(self, word: str) -> src.german_data_extract.GermanWordData:
        return await src.german_data_extract.prepare_data_for_german_word(word, hints=WordHints(""))


class TestGermanShortenPluralForm:
    def test_simple_ung(self):
        res = shorten_german_noun_plural_form_for_anki_card("Wohnung", "Wohnungen")
        assert "-en" == res

    def test_common_prefix(self):
        res = shorten_german_noun_plural_form_for_anki_card("Zeugnis", "Zeugnisse")
        assert "-se" == res

    def test_same(self):
        res = shorten_german_noun_plural_form_for_anki_card("Lehrer", "Lehrer")
        assert "=" == res

    def test_umlaut(self):
        res = shorten_german_noun_plural_form_for_anki_card("Apfel", "Äpfel")
        assert "die Äpfel" == res


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

    async def prepare_data(self, word: str) -> EnglishWordData:
        return await prepare_data_for_english_word(word, hints=WordHints(""))


class TestGetAudioFileNameForPhrase:
    def setup_method(self):
        random.seed(42)

    def test_de_word(self):
        res = get_audio_file_name_for_phrase("Katze", lang="de")
        assert "anki_card_generator_de_Katze_phrase_NbrnTP.mp3" == res

    def test_de_phrase(self):
        res = get_audio_file_name_for_phrase("sich in Träumerei vertiefen", lang="de")
        assert "anki_card_generator_de_sich_in_Träumerei_vertiefen_phrase_NbrnTP.mp3" == res

    def test_de_sentence(self):
        res = get_audio_file_name_for_sentence("Katze", lang="de")
        assert "anki_card_generator_de_Katze_sentence_NbrnTP.mp3" == res

    def test_de_word_with_slash(self):
        res = get_audio_file_name_for_sentence("sich/jdn. trösten", lang="de")
        assert "anki_card_generator_de_sich_jdn__trösten_sentence_NbrnTP.mp3" == res
