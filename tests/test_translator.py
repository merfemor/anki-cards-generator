import pytest

from app.translate import translate_text


@pytest.mark.asyncio(loop_scope="class")
class TestTranslator:
    async def test_simple_en_to_ru_translate(self):
        res = await translate_text("book", src="en", dest="ru")
        assert res.lower() == "книга"

    async def test_simple_de_to_ru_translate(self):
        res = await translate_text("Buch", src="de", dest="ru")
        assert res.lower() == "книга"
