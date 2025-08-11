import asyncio
import sys

import googletrans
import httpx


async def translate_text(text: str, src: str, dest: str) -> str:
    async with googletrans.Translator() as translator:
        res = await translator.translate(text, dest=dest, src=src)
        res_text: str = res.text
        return res_text


def check_translator_is_available() -> None:
    try:
        asyncio.run(translate_text("Katze", src="de", dest="ru"))
    except httpx.ConnectError:
        print("Error: Failed to connect to Google Translate. Check your internet connection.")
        sys.exit(1)
