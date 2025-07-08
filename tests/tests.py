import unittest

import src.german_data_extract
import src.utils
from src.german_data_extract import GermanWordData, PartOfSpeech


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
        expected = GermanWordData(original_word='Katze',
                                  pos_tag='NN',
                                  part_of_speech=PartOfSpeech.Noun,
                                  translated_en='cat',
                                  translated_ru='кот',
                                  noun_properties=src.german_data_extract.GermanNounProperties(
                                      singular_form='Katze',
                                      plural_form='Katzen',
                                      genus='f',
                                      article='die'),
                                  sentence_example='STUB',
                                  sentence_example_translated_en='Stub')
        self.assertEqual(expected, self.prepare_data("Katze"))

    def test_noun_no_plural(self):
        expected = GermanWordData(original_word='Schnee',
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

    def test_noun_no_singular(self):
        expected = GermanWordData(original_word='Ferien',
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
        expected = GermanWordData(original_word='Schwimmen',
                                  pos_tag='NNI',
                                  part_of_speech=PartOfSpeech.Noun,
                                  translated_en='to swim',
                                  translated_ru='плавать',
                                  noun_properties=src.german_data_extract.GermanNounProperties(
                                      singular_form='Schwimmen',
                                      plural_form='',
                                      genus='n',
                                      article='das'),
                                  sentence_example='STUB',
                                  sentence_example_translated_en='Stub')
        self.assertEqual(expected, self.prepare_data("Schwimmen"))

    def test_verb(self):
        expected = GermanWordData(original_word='schlafen',
                                  pos_tag='VV(INF)',
                                  part_of_speech=PartOfSpeech.Verb,
                                  translated_en='to sleep',
                                  translated_ru='спать',
                                  noun_properties=None,
                                  sentence_example='STUB',
                                  sentence_example_translated_en='Stub')
        self.assertEqual(expected, self.prepare_data("schlafen"))

    def test_adjective(self):
        expected = GermanWordData(original_word='lustig',
                                  pos_tag='ADJ(D)',
                                  part_of_speech=PartOfSpeech.Other,
                                  translated_en='funny',
                                  translated_ru='забавный',
                                  noun_properties=None,
                                  sentence_example='STUB',
                                  sentence_example_translated_en='Stub')
        self.assertEqual(expected, self.prepare_data("lustig"))

    def test_subordinating_conjunction(self):
        expected = GermanWordData(original_word='obgleich',
                                  pos_tag='KOUS',
                                  part_of_speech=PartOfSpeech.Other,
                                  translated_en='although',
                                  translated_ru='хотя',
                                  noun_properties=None,
                                  sentence_example='STUB',
                                  sentence_example_translated_en='Stub')
        self.assertEqual(expected, self.prepare_data("obgleich"))

    def test_coordinating_conjunction(self):
        expected = GermanWordData(original_word='und',
                                  pos_tag='KON',
                                  part_of_speech=PartOfSpeech.Other,
                                  translated_en='and',
                                  translated_ru='и',
                                  noun_properties=None,
                                  sentence_example='STUB',
                                  sentence_example_translated_en='Stub')
        self.assertEqual(expected, self.prepare_data("und"))

    def test_adverb(self):
        expected = GermanWordData(original_word='gerade',
                                  pos_tag='ADV',
                                  part_of_speech=PartOfSpeech.Other,
                                  translated_en='straight',
                                  translated_ru='прямой',
                                  noun_properties=None,
                                  sentence_example='STUB',
                                  sentence_example_translated_en='Stub')
        self.assertEqual(expected, self.prepare_data("gerade"))

    def test_preposition(self):
        expected = GermanWordData(original_word='durch',
                                  pos_tag='APPR',
                                  part_of_speech=PartOfSpeech.Other,
                                  translated_en='through',
                                  translated_ru='через',
                                  noun_properties=None,
                                  sentence_example='STUB',
                                  sentence_example_translated_en='Stub')
        self.assertEqual(expected, self.prepare_data("durch"))

    def test_collocation(self):
        with self.assertRaises(NotImplementedError):
            self.prepare_data("eine Entscheidung treffen")

    def test_rare_compound_word(self):
        with self.assertRaises(NotImplementedError):
            self.prepare_data("Kuddelmuddelkiste")

    def prepare_data(self, word: str) -> src.german_data_extract.GermanWordData:
        return src.german_data_extract.prepare_data_for_german_word(word, stub_ai=True)


if __name__ == '__main__':
    unittest.main()
