import os
import tempfile

from app import tts
from base_app_test import AbstractAppRestTest


class TestTextToSpeech(AbstractAppRestTest):
    def run_test(self, word: str, lang: str):
        with self.get_test_context():
            with tempfile.TemporaryDirectory() as tmp_dir:
                file_path = os.path.join(tmp_dir, "tts_test_file.mp3")
                tts.text_to_speech_into_file(word, file_path, lang=lang)
                assert os.path.exists(file_path)
                assert os.path.getsize(file_path) > 0

    def test_tts_works_for_german(self):
        self.run_test("die Katze", lang="de")

    def test_tts_works_for_english(self):
        self.run_test("cat", lang="en")
