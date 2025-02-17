from src.ai_interact import ask_ai
from src.translate import translate_text
from src.utils import check


def prepare_data_for_english_word(word: str) -> dict[str, str]:
    result = {
        "original_word": word,
        "translated_ru": translate_text(word, src="en", dest="ru").lower(),
    }
    en_sentence_example = get_english_sentence_example(word)
    result["sentence_example_en"] = en_sentence_example
    result["sentence_example_translated_ru"] = translate_text(en_sentence_example, src="en", dest="ru")
    return result


def get_english_sentence_example(word: str) -> str:
    prompt = f"Generate one simple sentence in English with the use of the word \"{word}\""

    res = ask_ai(prompt).strip()
    check(len(res) > len(word), f"Too short response: {res}")
    check(len(res) < 1000, f"Too long response, len={len(res)}")

    return res
