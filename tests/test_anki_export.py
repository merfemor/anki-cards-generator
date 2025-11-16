import os
import tempfile

from src import tts, german_anki_generate
from src.german_data_extract import GermanWordData, GermanNounProperties, PartOfSpeech


class TestWordDataExportToAnki:
    def setup_method(self):
        tts.init_tts_engine()

    def test_export_singe_de_word(self):
        katze_word_data = GermanWordData(
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
            german_anki_generate.export_results_to_anki_deck(word_data, file_path)
            assert os.path.getsize(file_path) > 0
