import random

from src.anki_common import get_audio_file_name_for_phrase, get_audio_file_name_for_sentence


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
