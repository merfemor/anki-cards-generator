import asyncio
import sys
from abc import ABC, abstractmethod

import googletrans
import httpx


class Translator(ABC):
    @abstractmethod
    async def translate_text(self, text: str, src: str, dest: str) -> str:
        pass


class GoogleTranslatorImpl(Translator):
    async def translate_text(self, text: str, src: str, dest: str) -> str:
        async with googletrans.Translator() as translator:
            res = await translator.translate(text, dest=dest, src=src)
            res_text: str = res.text
            return res_text


__GLOBAL_TRANSLATOR: Translator = GoogleTranslatorImpl()


async def translate_text(text: str, src: str, dest: str) -> str:
    global __GLOBAL_TRANSLATOR

    return await __GLOBAL_TRANSLATOR.translate_text(text, src, dest)


def override_global_translator_for_test(translator: Translator) -> None:
    global __GLOBAL_TRANSLATOR
    __GLOBAL_TRANSLATOR = translator


def check_translator_is_available() -> None:
    try:
        asyncio.run(__GLOBAL_TRANSLATOR.translate_text("Katze", src="de", dest="ru"))
    except httpx.ConnectError:
        print("Error: Failed to connect to Google Translate. Check your internet connection.")
        sys.exit(1)
