import logging
import subprocess
import sys
import tempfile
import wave
from abc import ABC, abstractmethod
from pathlib import Path

from flask import current_app
from piper import PiperVoice

from app.utils import check

PIPER_VOICES = {
    "de": "de_DE-thorsten-medium",
    "en": "en_US-lessac-medium",
}


class TextToSpeechEngine(ABC):
    @abstractmethod
    def text_to_speech_into_file(self, text: str, save_to_path: str, lang: str) -> None:
        pass


class PiperTextToSpeechEngine(TextToSpeechEngine):
    def __init__(self) -> None:
        self._model_dir = Path.home() / ".cache" / "anki-cards-generator" / "piper"
        self._model_dir.mkdir(parents=True, exist_ok=True)
        self._voices: dict[str, PiperVoice] = {}

        for lang, voice_name in PIPER_VOICES.items():
            model_path = self._model_dir / f"{voice_name}.onnx"
            config_path = self._model_dir / f"{voice_name}.onnx.json"
            if any(not path.is_file() or path.stat().st_size == 0 for path in (model_path, config_path)):
                logging.info("Downloading Piper voice: %s", voice_name)
                subprocess.run(
                    [
                        sys.executable,
                        "-m",
                        "piper.download_voices",
                        "--download-dir",
                        str(self._model_dir),
                        voice_name,
                    ],
                    check=True,
                )

            self._voices[lang] = PiperVoice.load(str(model_path))

    def _load_voice(self, lang: str) -> PiperVoice:
        try:
            return self._voices[lang]
        except KeyError as exc:
            raise ValueError(f"Unsupported language for Piper TTS: {lang}") from exc

    def text_to_speech_into_file(self, text: str, save_to_path: str, lang: str) -> None:
        voice = self._load_voice(lang)
        with tempfile.TemporaryDirectory() as temp_dir:
            wav_path = Path(temp_dir) / "speech.wav"
            with wave.open(str(wav_path), "wb") as wav_file:
                voice.synthesize_wav(text, wav_file)
            subprocess.run(["lame", "--quiet", "-b", "128", str(wav_path), save_to_path], check=True)


def init_tts_engine() -> TextToSpeechEngine:
    logging.info("Using Piper as text-to-speech engine")
    return PiperTextToSpeechEngine()


def text_to_speech_into_file(text: str, save_to_path: str, lang: str) -> None:
    check(save_to_path.endswith(".mp3"), f"Expected path to end with .mp3 extension, but got {save_to_path}")

    logging.debug(f"Generate text to speech for text={text} in lang={lang} into {save_to_path}")
    tts_engine: TextToSpeechEngine = current_app.extensions["tts_engine"]
    tts_engine.text_to_speech_into_file(text, save_to_path, lang)
