import asyncio
import logging
import os
import sys
from abc import ABC, abstractmethod

import deepl
import httpx


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


__GLOBAL_TRANSLATOR: Translator


async def translate_text(text: str, src: str, dest: str) -> str:
    global __GLOBAL_TRANSLATOR

    return await __GLOBAL_TRANSLATOR.translate_text(text, src, dest)


def override_global_translator_for_test(translator: Translator) -> None:
    global __GLOBAL_TRANSLATOR
    __GLOBAL_TRANSLATOR = translator


def init_translator() -> None:
    global __GLOBAL_TRANSLATOR
    logging.info("Using DeepL API as a translator.")
    __GLOBAL_TRANSLATOR = DeeplTranslatorImpl()
    check_translator_is_available()


def check_translator_is_available() -> None:
    try:
        asyncio.run(__GLOBAL_TRANSLATOR.translate_text("Katze", src="de", dest="ru"))
    except httpx.ConnectError:
        print("Error: Failed to connect to translator. Check your internet connection.")
        sys.exit(1)
