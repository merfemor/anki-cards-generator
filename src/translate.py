import asyncio
import googletrans


def translate_text(text: str, src: str = "de", dest: str = "en") -> str:
    async def execute() -> str:
        async with googletrans.Translator() as translator:
            res = await translator.translate(text, dest=dest, src=src)
            return res.text

    return asyncio.run(execute())
