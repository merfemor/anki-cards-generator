import pytest
from dotenv import load_dotenv

from app.translate import translate_text, init_translator


@pytest.mark.asyncio(loop_scope="class")
class TestTranslator:
    def setup_method(self):
        load_dotenv()
        init_translator()

    async def test_simple_en_to_ru_translate(self):
        res = await translate_text("book", src="en", dest="ru")
        assert res.lower() == "книга"

    async def test_simple_de_to_ru_translate(self):
        res = await translate_text("Buch", src="de", dest="ru")
        assert res.lower() == "книга"
