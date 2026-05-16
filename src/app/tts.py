import logging
import platform
import subprocess
import tempfile
from abc import ABC, abstractmethod

from app.utils import check


class TextToSpeechEngine(ABC):
    @abstractmethod
    def text_to_speech_into_file(self, text: str, save_to_path: str, lang: str) -> None:
        pass


def check_command_exists(command: str) -> None:
    check(
        subprocess.run(["which", command], capture_output=True).returncode == 0,
        f"Command '{command}' is not found. It is required for Mac TTS engine",
    )


class MacTextToSpeechEngineImpl(TextToSpeechEngine):
    def __init__(self) -> None:
        check(
            platform.system() == "Darwin",
            f"Mac TTS engine is only supported on macOS, but current OS is {platform.system()}",
        )
        check_command_exists("say")
        check_command_exists("lame")

    def text_to_speech_into_file(self, text: str, save_to_path: str, lang: str) -> None:
        if lang == "de":
            voice = "Anna"
        elif lang == "en":
            voice = "Samantha"
        else:
            raise ValueError(f"Unsupported language for Mac TTS: {lang}")

        with tempfile.NamedTemporaryFile(mode="wb", suffix=".aiff") as temp_aiff:
            temp_aiff_path = temp_aiff.name
            subprocess.run(["say", "-v", voice, "-o", temp_aiff_path, text], check=True)
            subprocess.run(["lame", "--quiet", "-b", "128", temp_aiff_path, save_to_path], check=True)


__TTS_ENGINE: TextToSpeechEngine


def init_tts_engine() -> None:
    global __TTS_ENGINE
    logging.info("Using Mac 'say' as text-to-speech engine")
    __TTS_ENGINE = MacTextToSpeechEngineImpl()


def text_to_speech_into_file(text: str, save_to_path: str, lang: str) -> None:
    check(save_to_path.endswith(".mp3"), f"Expected path to end with .mp3 extension, but got {save_to_path}")

    logging.info(f"Generate text to speech for text={text} in lang={lang} into {save_to_path}")
    __TTS_ENGINE.text_to_speech_into_file(text, save_to_path, lang)
