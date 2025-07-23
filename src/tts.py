from gtts import gTTS

from src.utils import check


def text_to_speech_into_file(text: str, save_to_path: str, lang: str) -> None:
    check(save_to_path.endswith(".mp3"), f"Expected path to end with .mp3 extension, but got {save_to_path}")

    tts = gTTS(text=text, lang=lang)
    tts.save(save_to_path)
