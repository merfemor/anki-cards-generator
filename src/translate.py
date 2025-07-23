import googletrans

async def translate_text(text: str, src: str, dest: str) -> str:
    async with googletrans.Translator() as translator:
        res = await translator.translate(text, dest=dest, src=src)
        res_text: str = res.text
        return res_text
