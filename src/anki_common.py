import random
import string


def get_audio_file_name_for_phrase(phrase: str, lang: str) -> str:
    return _get_audio_file_name_for_common(phrase, lang, "phrase")


def get_audio_file_name_for_sentence(phrase: str, lang: str) -> str:
    return _get_audio_file_name_for_common(phrase, lang, "sentence")


def _get_audio_file_name_for_common(phrase: str, lang: str, content_type: str) -> str:
    phrase_no_space = phrase.replace(" ", "_")
    # Doing our best to protect from audio file name collisions
    random_suffix = _generate_random_string(length=6)
    return f"anki_card_generator_{lang}_{phrase_no_space}_{content_type}_{random_suffix}.mp3"


def _generate_random_string(length: int) -> str:
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))
