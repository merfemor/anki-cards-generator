import unittest

import src.german_data_extract
import src.utils
from src.german_data_extract import GermanWordData, PartOfSpeech


class GermanPosTagTestCase(unittest.TestCase):
    def test_empty_string(self):
        with self.assertRaises(ValueError):
            src.german_data_extract.get_pos_tag_of_german_word("")

    def test_noun(self):
        tag: str = src.german_data_extract.get_pos_tag_of_german_word("Katze")
        self.assertEqual("NN", tag)

    def test_verb_infinitive(self):
        tag: str = src.german_data_extract.get_pos_tag_of_german_word("schlafen")
        self.assertEqual("VV(INF)", tag)

    def test_adjective(self):
        tag: str = src.german_data_extract.get_pos_tag_of_german_word("lustig")
        self.assertEqual("ADJ(D)", tag)

    def test_conjunction(self):
        tag: str = src.german_data_extract.get_pos_tag_of_german_word("und")
        self.assertEqual("KON", tag)

    def test_noun_ambiguity_with_verb(self):
        tag: str = src.german_data_extract.get_pos_tag_of_german_word("Schwimmen")
        self.assertEqual("NNI", tag)

    def test_spaces(self):
        with self.assertRaises(ValueError):
            src.german_data_extract.get_pos_tag_of_german_word("    ")


class GermanPrepareDataTestCase(unittest.TestCase):
    def test_noun(self):
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

    def prepare_data(self, word: str) -> src.german_data_extract.GermanWordData:
        return src.german_data_extract.prepare_data_for_german_word(word, stub_ai=True)


if __name__ == '__main__':
    unittest.main()
