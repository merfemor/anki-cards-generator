import os
import tempfile

from app import german_anki_generate
from app.german_data_extract import GermanWordData, GermanNounProperties, PartOfSpeech
from base_app_test import AbstractAppRestTest


class TestWordDataExportToAnki(AbstractAppRestTest):
    def test_export_singe_de_word(self):
        katze_word_data = GermanWordData(
            raw_word="die Katze",
            word="die Katze",
            pos_tag="NN",
            part_of_speech=PartOfSpeech.Noun,
            translated_en="cat",
            translated_ru="кошка",
            noun_properties=GermanNounProperties(
                singular_form="Katze",
                plural_form="Katzen",
                genus="f",
                article="die",
            ),
            sentence_example="Satz Beispiel",
            sentence_example_translated_en="sentence example",
            word_note_suffix="",
        )
        word_data = [katze_word_data]

        with tempfile.NamedTemporaryFile(suffix=".apkg") as tmp_file:
            file_path = tmp_file.name
            assert os.path.getsize(file_path) == 0
            self.run_export(word_data, file_path)
            assert os.path.getsize(file_path) > 0

    def run_export(self, word_data, file_path: str) -> None:
        with self.get_test_context():
            german_anki_generate.export_results_to_anki_deck(word_data, file_path)
