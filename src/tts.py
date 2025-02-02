from gtts import gTTS

from src.utils import check


def german_text_to_speech(text: str, save_to_path: str):
    check(save_to_path.endswith(".mp3"), f"Expected path to end with .mp3 extension, but got {save_to_path}")

    tts = gTTS(text=text, lang='de')
    tts.save(save_to_path)
