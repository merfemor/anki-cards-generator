import random
import re
import string


def get_audio_file_name_for_phrase(phrase: str, lang: str) -> str:
    return _get_audio_file_name_for_common(phrase, lang, "phrase")


def get_audio_file_name_for_sentence(phrase: str, lang: str) -> str:
    return _get_audio_file_name_for_common(phrase, lang, "sentence")


def sanitize_string(s: str) -> str:
    return re.sub(r"[^a-zöüäßA-ZÖÜÄ0-9\-_]", "_", s.strip())


def _get_audio_file_name_for_common(phrase: str, lang: str, content_type: str) -> str:
    phrase = sanitize_string(phrase)
    # Doing our best to protect from audio file name collisions
    random_suffix = _generate_random_string(length=6)
    return f"anki_card_generator_{lang}_{phrase}_{content_type}_{random_suffix}.mp3"


def _generate_random_string(length: int) -> str:
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))
