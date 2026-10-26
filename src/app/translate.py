import logging
import os
import sys
from abc import ABC, abstractmethod

import deepl
from flask import current_app


class Translator(ABC):
    @abstractmethod
    async def translate_text(self, text: str, src: str, dest: str) -> str:
        pass


class DeeplTranslatorImpl(Translator):
    def __init__(self) -> None:
        api_key = os.environ.get("DEEPL_API_KEY")
        if api_key is None:
            print("Error: DEEPL_API_KEY env variable is not set.")
            sys.exit(1)
        self.__init_(api_key)

    def __init_(self, api_key: str) -> None:
        self.translator = deepl.DeepLClient(api_key)

    async def translate_text(self, text: str, src: str, dest: str) -> str:
        if dest == "en":
            # Target lang=en is deprecated
            return await self.translate_text(text, src, "en-us")

        try:
            return self.translator.translate_text(text, source_lang=src, target_lang=dest).text
        except deepl.QuotaExceededException as e:
            logging.error(
                "DeepL API translation quota exceeded. Check your account at https://www.deepl.com/en/your-account/usage for details."
            )
            raise e
        except deepl.DeepLException as e:
            logging.error(f'Failed to translate {src}->{dest} text: "{text}".')
            raise e


async def translate_text(text: str, src: str, dest: str) -> str:
    translator: Translator = current_app.extensions["translator"]
    return await translator.translate_text(text, src, dest)


def init_translator() -> Translator:
    logging.info("Using DeepL API as a translator.")
    return DeeplTranslatorImpl()
