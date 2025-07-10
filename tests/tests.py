import unittest

import src.german_data_extract
import src.utils
from src.english_data_extract import prepare_data_for_english_word, EnglishWordData
from src.german_anki_generate import shorten_german_noun_plural_form_for_anki_card
from src.german_data_extract import GermanWordData, PartOfSpeech
from src.translate import translate_text
from src.word_hints import WordHints


class GermanPrepareDataTestCase(unittest.TestCase):
    def test_empty_string(self):
        with self.assertRaises(ValueError):
            self.prepare_data("")

    def test_spaces_string(self):
        with self.assertRaises(ValueError):
            self.prepare_data("   ")

    def test_non_words_symbol(self):
        with self.assertRaises(ValueError):
            self.prepare_data("$")

    def test_non_words_dot(self):
        with self.assertRaises(ValueError):
            self.prepare_data(".")

    def test_non_words_comma(self):
        with self.assertRaises(ValueError):
            self.prepare_data(",")

    def test_non_words_dash(self):
        with self.assertRaises(ValueError):
            self.prepare_data("-")

    def test_noun_feminine(self):
        expected = GermanWordData(word_infinitive='Katze',
                                  pos_tag='NN',
                                  part_of_speech=PartOfSpeech.Noun,
                                  translated_en='cat',
                                  translated_ru='кошка',
                                  noun_properties=src.german_data_extract.GermanNounProperties(
                                      singular_form='Katze',
                                      plural_form='Katzen',
                                      genus='f',
                                      article='die'),
                                  sentence_example='STUB',
                                  sentence_example_translated_en='Stub')
        self.assertEqual(expected, self.prepare_data("Katze"))

    def test_noun_no_plural(self):
        expected = GermanWordData(word_infinitive='Schnee',
                                  pos_tag='NN',
                                  part_of_speech=PartOfSpeech.Noun,
                                  translated_en='snow',
                                  translated_ru='снег',
                                  noun_properties=src.german_data_extract.GermanNounProperties(
                                      singular_form='Schnee',
                                      plural_form='',
                                      genus='m',
                                      article='der'),
                                  sentence_example='STUB',
                                  sentence_example_translated_en='Stub')
        self.assertEqual(expected, self.prepare_data("Schnee"))

    def test_noun_two_plural(self):
        expected = GermanWordData(word_infinitive='Band',
                                  pos_tag='NN',
                                  part_of_speech=PartOfSpeech.Noun,
                                  translated_en='tape',
                                  translated_ru='лента',
                                  noun_properties=src.german_data_extract.GermanNounProperties(
                                      singular_form='Band',
                                      plural_form='Bänder',
                                      genus='n',
                                      article='das'),
                                  sentence_example='STUB',
                                  sentence_example_translated_en='Stub')
        self.assertEqual(expected, self.prepare_data("Band"))

    def test_noun_no_singular(self):
        expected = GermanWordData(word_infinitive='Ferien',
                                  pos_tag='NN',
                                  part_of_speech=PartOfSpeech.Noun,
                                  translated_en='holidays',
                                  translated_ru='праздники',
                                  noun_properties=src.german_data_extract.GermanNounProperties(
                                      singular_form='',
                                      plural_form='Ferien',
                                      genus='pl',
                                      article='die'),
                                  sentence_example='STUB',
                                  sentence_example_translated_en='Stub')
        self.assertEqual(expected, self.prepare_data("Ferien"))

    def test_noun_ambiguity_with_verb(self):
        expected = GermanWordData(word_infinitive='Schwimmen',
                                  pos_tag='NNI',
                                  part_of_speech=PartOfSpeech.Noun,
                                  translated_en='swimming',
                                  translated_ru='плавание',
                                  noun_properties=src.german_data_extract.GermanNounProperties(
                                      singular_form='Schwimmen',
                                      plural_form='',
                                      genus='n',
                                      article='das'),
                                  sentence_example='STUB',
                                  sentence_example_translated_en='Stub')
        self.assertEqual(expected, self.prepare_data("Schwimmen"))

    def test_verb(self):
        expected = GermanWordData(word_infinitive='schlafen',
                                  pos_tag='VV(INF)',
                                  part_of_speech=PartOfSpeech.Verb,
                                  translated_en='to sleep',
                                  translated_ru='спать',
                                  noun_properties=None,
                                  sentence_example='STUB',
                                  sentence_example_translated_en='Stub')
        self.assertEqual(expected, self.prepare_data("schlafen"))

    def test_adjective(self):
        expected = GermanWordData(word_infinitive='lustig',
                                  pos_tag='ADJ(D)',
                                  part_of_speech=PartOfSpeech.Other,
                                  translated_en='funny',
                                  translated_ru='забавный',
                                  noun_properties=None,
                                  sentence_example='STUB',
                                  sentence_example_translated_en='Stub')
        self.assertEqual(expected, self.prepare_data("lustig"))

    def test_subordinating_conjunction(self):
        expected = GermanWordData(word_infinitive='obgleich',
                                  pos_tag='KOUS',
                                  part_of_speech=PartOfSpeech.Other,
                                  translated_en='although',
                                  translated_ru='хотя',
                                  noun_properties=None,
                                  sentence_example='STUB',
                                  sentence_example_translated_en='Stub')
        self.assertEqual(expected, self.prepare_data("obgleich"))

    def test_coordinating_conjunction(self):
        expected = GermanWordData(word_infinitive='und',
                                  pos_tag='KON',
                                  part_of_speech=PartOfSpeech.Other,
                                  translated_en='and',
                                  translated_ru='и',
                                  noun_properties=None,
                                  sentence_example='STUB',
                                  sentence_example_translated_en='Stub')
        self.assertEqual(expected, self.prepare_data("und"))

    def test_adverb(self):
        expected = GermanWordData(word_infinitive='gerade',
                                  pos_tag='ADV',
                                  part_of_speech=PartOfSpeech.Other,
                                  translated_en='straight',
                                  translated_ru='прямой',
                                  noun_properties=None,
                                  sentence_example='STUB',
                                  sentence_example_translated_en='Stub')
        self.assertEqual(expected, self.prepare_data("gerade"))

    def test_with_hint(self):
        expected = GermanWordData(word_infinitive='lustig',
                                  pos_tag='ADJ(D)',
                                  part_of_speech=PartOfSpeech.Other,
                                  translated_en='funny',
                                  translated_ru='смешной, весёлый',
                                  noun_properties=None,
                                  sentence_example='STUB',
                                  sentence_example_translated_en='Stub')
        self.assertEqual(expected, src.german_data_extract.prepare_data_for_german_word("lustig", hints=WordHints("смешной, весёлый"), stub_ai=True))

    def test_preposition(self):
        expected = GermanWordData(word_infinitive='durch',
                                  pos_tag='APPR',
                                  part_of_speech=PartOfSpeech.Other,
                                  translated_en='through',
                                  translated_ru='через',
                                  noun_properties=None,
                                  sentence_example='STUB',
                                  sentence_example_translated_en='Stub')
        self.assertEqual(expected, self.prepare_data("durch"))

    def test_collocation(self):
        expected = GermanWordData(word_infinitive='eine Entscheidung treffen',
                                  pos_tag='',
                                  part_of_speech=PartOfSpeech.Other,
                                  translated_en='make a decision',
                                  translated_ru='принять решение',
                                  noun_properties=None,
                                  sentence_example='STUB',
                                  sentence_example_translated_en='Stub')
        self.assertEqual(expected, self.prepare_data("eine Entscheidung treffen"))

    def test_rare_compound_word(self):
        with self.assertRaises(NotImplementedError):
            self.prepare_data("Kuddelmuddelkiste")

    def test_noun_with_article_given(self):
        expected = GermanWordData(word_infinitive='Katze',
                                  pos_tag='NN',
                                  part_of_speech=PartOfSpeech.Noun,
                                  translated_en='cat',
                                  translated_ru='кошка',
                                  noun_properties=src.german_data_extract.GermanNounProperties(
                                      singular_form='Katze',
                                      plural_form='Katzen',
                                      genus='f',
                                      article='die'),
                                  sentence_example='STUB',
                                  sentence_example_translated_en='Stub')
        self.assertEqual(expected, self.prepare_data("die Katze"))


    def test_noun_in_plural_given(self):
        expected = GermanWordData(word_infinitive='Markt',
                                  pos_tag='NN',
                                  part_of_speech=PartOfSpeech.Noun,
                                  translated_en='market',
                                  translated_ru='рынок',
                                  noun_properties=src.german_data_extract.GermanNounProperties(
                                      singular_form='Markt',
                                      plural_form='Märkte',
                                      genus='m',
                                      article='der'),
                                  sentence_example='STUB',
                                  sentence_example_translated_en='Stub')
        self.assertEqual(expected, self.prepare_data("Märkte"))


    def test_adjective_conjugated_given(self):
        expected = GermanWordData(word_infinitive='schnell',
                                  pos_tag='ADJ(A)',
                                  part_of_speech=PartOfSpeech.Other,
                                  translated_en='fast',
                                  translated_ru='быстрый',
                                  noun_properties=None,
                                  sentence_example='STUB',
                                  sentence_example_translated_en='Stub')
        self.assertEqual(expected, self.prepare_data("schnelle"))

    def test_noun_with_mistake_given(self):
        with self.assertRaises(NotImplementedError):
            self.prepare_data("Erfarung")

    def test_verb_with_mistake_given(self):
        expected = GermanWordData(word_infinitive='empfeln',
                                  pos_tag='VV(INF)',
                                  part_of_speech=PartOfSpeech.Verb,
                                  translated_en='to reclaim',
                                  translated_ru='вернуть',
                                  noun_properties=None,
                                  sentence_example='STUB',
                                  sentence_example_translated_en='Stub')
        self.assertEqual(expected, self.prepare_data("empfelen"))

    def test_reflexive_verb(self):
        expected = GermanWordData(word_infinitive='sich interessieren',
                                  pos_tag='VV(INF)',
                                  part_of_speech=PartOfSpeech.Verb,
                                  translated_en='to interested in',
                                  translated_ru='увлекающийся',
                                  noun_properties=None,
                                  sentence_example='STUB',
                                  sentence_example_translated_en='Stub')
        self.assertEqual(expected, self.prepare_data('sich interessieren'))

    def test_rare_adjective(self):
        # Identified as FM = Fremdsprachliches Material
        expected = GermanWordData(word_infinitive='perplex',
                                  pos_tag='FM',
                                  part_of_speech=PartOfSpeech.Other,
                                  translated_en='perplexed',
                                  translated_ru='озадачен',
                                  noun_properties=None,
                                  sentence_example='STUB',
                                  sentence_example_translated_en='Stub')
        self.assertEqual(expected, self.prepare_data("perplex"))


    def prepare_data(self, word: str) -> src.german_data_extract.GermanWordData:
        return src.german_data_extract.prepare_data_for_german_word(word, hints=WordHints(""), stub_ai=True)


class GermanShortenPluralForm(unittest.TestCase):
    def test_simple_ung(self):
        res = shorten_german_noun_plural_form_for_anki_card("Wohnung", "Wohnungen")
        self.assertEqual("-en", res)

    def test_common_prefix(self):
        res = shorten_german_noun_plural_form_for_anki_card("Zeugnis", "Zeugnisse")
        self.assertEqual("-se", res)

    def test_same(self):
        res = shorten_german_noun_plural_form_for_anki_card("Lehrer", "Lehrer")
        self.assertEqual("=", res)

    def test_umlaut(self):
        res = shorten_german_noun_plural_form_for_anki_card("Apfel", "Äpfel")
        self.assertEqual("die Äpfel", res)


class EnglishPrepareDataTestCase(unittest.TestCase):
    def test_empty_word(self):
        with self.assertRaises(ValueError):
            self.prepare_data("")

    def test_spaces(self):
        with self.assertRaises(ValueError):
            self.prepare_data("     ")

    def test_noun(self):
        expected = EnglishWordData(
            original_word='cat',
            translated='кот',
            sentence_example='',
            sentence_example_translated='',
        )
        self.assertEqual(expected, self.prepare_data("cat"))

    def test_verb(self):
        expected = EnglishWordData(
            original_word='swim',
            translated='плавать',
            sentence_example='',
            sentence_example_translated='',
        )
        self.assertEqual(expected, self.prepare_data("swim"))

    def test_verb_with_to(self):
        expected = EnglishWordData(
            original_word='to swim',
            translated='плавать',
            sentence_example='',
            sentence_example_translated='',
        )
        self.assertEqual(expected, self.prepare_data("to swim"))

    def test_phrasal_verb(self):
        expected = EnglishWordData(
            original_word='cut off',
            translated='отрезать',
            sentence_example='',
            sentence_example_translated='',
        )
        self.assertEqual(expected, self.prepare_data("cut off"))


    def test_phrasal_verb_with_to(self):
        expected = EnglishWordData(
            original_word='to cut off',
            translated='чтобы отрезать',
            sentence_example='',
            sentence_example_translated='',
        )
        self.assertEqual(expected, self.prepare_data("to cut off"))

    def test_adjective(self):
        expected = EnglishWordData(
            original_word='miscellaneous',
            translated='разнообразный',
            sentence_example='',
            sentence_example_translated='',
        )
        self.assertEqual(expected, self.prepare_data("miscellaneous"))

    def test_with_hint(self):
        expected = EnglishWordData(
            original_word='miscellaneous',
            translated='смешанный, разнообразный',
            sentence_example='',
            sentence_example_translated='',
        )
        self.assertEqual(expected, prepare_data_for_english_word("miscellaneous", WordHints("смешанный, разнообразный"), stub_llm=True))

    def prepare_data(self, word: str) -> EnglishWordData:
        return prepare_data_for_english_word(word, hints=WordHints(""), stub_llm=True)


class LocalTranslatorTestCase(unittest.TestCase):
    def test_translate_en_to_ru_text(self):
        actual = translate_text("The severe storm cut off power to a large section of the city.", src="en", dest="ru")
        self.assertEqual("Сильный шторм перерезал власть до большой части города.", actual)

    def test_translate_de_to_ru_text(self):
        sentence_de = "Dass sie trotz der ihr von mehreren Seiten angebotenen Hilfe weiterhin darauf bestand, alles allein zu erledigen, hat nicht nur ihre Freunde überrascht, sondern auch zu Spannungen innerhalb der Gruppe geführt."
        actual = translate_text(sentence_de, src="de", dest="ru")
        self.assertEqual("Тот факт, что, несмотря на помощь, предлагаемую несколькими сторонами, она продолжала настаивать на том, чтобы делать все в одиночестве, не только удивлен ее друзьями, но и приводила к напряженности в группе.", actual)

    def test_translate_single_word_de_to_ru(self):
        actual = translate_text("das Schwimmen", src="de", dest="ru")
        self.assertEqual("плавание", actual)

    def test_translate_single_word_de_to_en(self):
        actual = translate_text("das Schwimmen", src="de", dest="en")
        self.assertEqual("swimming", actual)

    def test_translate_single_word_de_to_ru_2(self):
        actual = translate_text("die Katze", src="de", dest="ru")
        self.assertEqual("Кошка", actual)

    def test_translate_single_word_de_to_en_2(self):
        actual = translate_text("der Markt", src="de", dest="en")
        self.assertEqual("The market", actual)

