import asyncio
import logging
import os
import sys
import tempfile
import threading
import webbrowser
from collections.abc import Callable
from typing import Tuple, Coroutine, TypeVar

from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_file, render_template, Response
from pydantic import ValidationError

from app import english_anki_generate
from app import german_anki_generate
from app.api_payload import GenerateCardsFilePayload, WordPayload
from app.configuration import parse_arguments
from app.english_data_extract import prepare_data_for_english_word, EnglishWordData
from app.german_data_extract import prepare_data_for_german_word, GermanWordData
from app.llm_interact import set_global_llm_provider
from app.translate import init_translator
from app.tts import init_tts_engine
from app.word_hints import WordHints

app = Flask(__name__)


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
    logging.getLogger("httpx").setLevel(logging.CRITICAL)
    logging.getLogger("deepl").setLevel(logging.WARNING)


def invalid_payload_response(exc: ValidationError) -> Tuple[Response, int]:
    details = [
        {"field": ".".join(str(part) for part in error["loc"]), "message": error["msg"]} for error in exc.errors()
    ]
    logging.debug(f"Request payload validation failed: {details}")
    return jsonify({"error": "Invalid request payload", "details": details}), 400


@app.route("/api/generateCardsFile", methods=["POST"])
async def generate_cards_file() -> Tuple[Response, int] | Response:
    try:
        payload = GenerateCardsFilePayload.model_validate(request.get_json(silent=True))
    except ValidationError as exc:
        return invalid_payload_response(exc)

    words = payload.words
    if not words:
        return jsonify({"error": 'The "words" list cannot be empty'}), 400

    language = payload.language
    if language == "de":
        logging.debug(f"Preparing German card data for the words {words}")
        return await common_generate_cards_file(
            words,
            prepare_data_fn=prepare_data_for_german_word,
            export_fn=german_anki_generate.export_results_to_anki_deck,
            file_suffix="to_import_german_anki_generated.apkg",
        )
    elif language == "en":
        logging.debug(f"Preparing English card data for the words {words}")
        return await common_generate_cards_file(
            words,
            prepare_data_fn=prepare_data_for_english_word,
            export_fn=english_anki_generate.export_results_to_anki_deck,
            file_suffix="to_import_english_anki_generated.apkg",
        )
    else:
        return jsonify({"error": f"Expected language to be one of 'en', 'de', but got '{language}'"}), 400


WD = TypeVar("WD", GermanWordData, EnglishWordData)


async def common_generate_cards_file(
    words: list[WordPayload],
    prepare_data_fn: Callable[[str, WordHints], Coroutine[None, None, WD]],
    export_fn: Callable[[list[WD], str], None],
    file_suffix: str,
) -> Response:
    tasks = [asyncio.create_task(prepare_data_fn(entry.word, entry.to_word_hints())) for entry in words]

    results = await asyncio.gather(*tasks)

    with tempfile.NamedTemporaryFile(delete=False, suffix=file_suffix) as temp_file:
        deck_filename = temp_file.name

    logging.debug(f'Exporting the results into the temporary Anki deck file "{deck_filename}"')
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
            logging.debug(f'Removed temporary Anki deck file "{deck_filename}"')


@app.route("/", methods=["GET"])
def home() -> str:
    return render_template("index.html")


def open_in_browser(*, url: str, after_seconds: int) -> None:
    threading.Timer(after_seconds, lambda: webbrowser.open_new(url)).start()


def main():
    load_dotenv()
    setup_logging()
    args = parse_arguments()
    set_global_llm_provider(args.llm_provider)
    init_tts_engine()
    init_translator()
    open_in_browser(url="http://127.0.0.1:5000/", after_seconds=1)
    app.run(port=5000)
