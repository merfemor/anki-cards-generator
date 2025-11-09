import logging
from abc import ABC, abstractmethod

from gtts import gTTS

from src.utils import check


class TextToSpeechEngine(ABC):
    @abstractmethod
    def text_to_speech_into_file(self, text: str, save_to_path: str, lang: str) -> None:
        pass


class GoogleTextToSpeechEngineImpl(TextToSpeechEngine):
    def text_to_speech_into_file(self, text: str, save_to_path: str, lang: str) -> None:
        tts = gTTS(text=text, lang=lang)
        tts.save(save_to_path)


__TTS_ENGINE: TextToSpeechEngine


def init_tts_engine() -> None:
    global __TTS_ENGINE
    logging.info("Using gTTS as text-to-speech engine")
    __TTS_ENGINE = GoogleTextToSpeechEngineImpl()


def text_to_speech_into_file(text: str, save_to_path: str, lang: str) -> None:
    check(save_to_path.endswith(".mp3"), f"Expected path to end with .mp3 extension, but got {save_to_path}")

    logging.info(f"Generate text to speech for text={text} in lang={lang} into {save_to_path}")
    __TTS_ENGINE.text_to_speech_into_file(text, save_to_path, lang)
