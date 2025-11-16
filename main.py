import asyncio
import logging
import os
import sys
import tempfile
import threading
import webbrowser
from collections.abc import Callable
from typing import Any, Tuple, Coroutine

from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_file, render_template, Response

import src.english_anki_generate
import src.german_anki_generate
from src.configuration import parse_arguments
from src.english_data_extract import prepare_data_for_english_word, EnglishWordData
from src.german_data_extract import prepare_data_for_german_word, GermanWordData
from src.llm_interact import set_global_llm_provider
from src.tts import init_tts_engine
from src.word_hints import WordHints
from src.translate import check_translator_is_available

app = Flask(__name__)


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
    logging.getLogger("httpx").setLevel(logging.CRITICAL)


def parse_hints_from_dict(word_with_context: dict[str, dict[str, str]]) -> WordHints:
    hints: dict[str, str] = word_with_context.get("hints", {})
    translated_ru: str = hints.get("translated_ru", "")
    translated_ru = translated_ru.strip()
    return WordHints(translated_ru)


@app.route("/api/generateCardsFile", methods=["POST"])
async def generate_cards_file() -> Tuple[Response, int] | Response:
    words_with_hints = request.get_json().get("words", [])
    if not words_with_hints:
        return jsonify({"error": 'The "words" list cannot be empty'}), 400

    language = request.get_json().get("language")

    if language == "de":
        logging.info(f"Preparing German card data for the words {words_with_hints}")
        return await common_generate_cards_file(
            words_with_hints,
            prepare_data_fn=prepare_data_for_german_word,
            export_fn=src.german_anki_generate.export_results_to_anki_deck,
            file_suffix="to_import_german_anki_generated.apkg",
        )
    elif language == "en":
        logging.info(f"Preparing English card data for the words {words_with_hints}")
        return await common_generate_cards_file(
            words_with_hints,
            prepare_data_fn=prepare_data_for_english_word,
            export_fn=src.english_anki_generate.export_results_to_anki_deck,
            file_suffix="to_import_english_anki_generated.apkg",
        )
    else:
        return jsonify({"error": f"Expected language to be one of 'en', 'de', but got '{language}'"}), 400


async def common_generate_cards_file[WD: GermanWordData | EnglishWordData](
    words_with_hints: list[dict[str, Any]],
    prepare_data_fn: Callable[[str, WordHints], Coroutine[None, None, WD]],
    export_fn: Callable[[list[WD], str], None],
    file_suffix: str,
) -> Tuple[Response, int] | Response:
    tasks = []
    for word_with_hints in words_with_hints:
        word: str = word_with_hints.get("word", "")
        word = word.strip()
        if not word:
            return jsonify({"error": f"The word is not specified for the word {word}"}), 400

        hints = parse_hints_from_dict(word_with_hints)
        task = asyncio.create_task(prepare_data_fn(word, hints))
        tasks.append(task)

    results = await asyncio.gather(*tasks)

    with tempfile.NamedTemporaryFile(delete=False, suffix=file_suffix) as temp_file:
        deck_filename = temp_file.name

    logging.info(f'Exporting the results into the temporary Anki deck file "{deck_filename}"')
    try:
        export_fn(results, deck_filename)

        response = send_file(
            deck_filename,
            as_attachment=True,
            download_name=os.path.basename(deck_filename),
            mimetype="application/octet-stream",
        )
        return response
    finally:
        if os.path.exists(deck_filename):
            os.remove(deck_filename)
            logging.info(f'Removed temporary Anki deck file "{deck_filename}"')


@app.route("/", methods=["GET"])
def home() -> str:
    return render_template("index.html")


def open_in_browser(*, url: str, after_seconds: int) -> None:
    threading.Timer(after_seconds, lambda: webbrowser.open_new(url)).start()


if __name__ == "__main__":
    load_dotenv()
    setup_logging()
    args = parse_arguments()
    set_global_llm_provider(args.llm_provider)
    init_tts_engine()
    check_translator_is_available()
    open_in_browser(url="http://127.0.0.1:5000/", after_seconds=1)
    app.run(port=5000)
