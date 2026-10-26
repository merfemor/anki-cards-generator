import logging
import os
import sys
import tempfile
import threading
import webbrowser
from collections.abc import Callable
from typing import Any, Tuple, TypeVar

from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_file, render_template, Response
from pydantic import ValidationError

from app import english_anki_generate
from app import german_anki_generate
from app.api_payload import ExportDeckFilePayload, GenerateWordDataPayload
from app.english_data_extract import prepare_data_for_english_word, EnglishWordData
from app.german_data_extract import prepare_data_for_german_word, GermanWordData
from app.llm_interact import init_llm_provider
from app.translate import init_translator
from app.tts import init_tts_engine

app = Flask(__name__)


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
    logging.getLogger("httpx").setLevel(logging.CRITICAL)
    logging.getLogger("deepl").setLevel(logging.WARNING)
    logging.getLogger("google_genai.models").setLevel(logging.WARNING)


def invalid_payload_response(exc: ValidationError) -> Tuple[Response, int]:
    details = [
        {"field": ".".join(str(part) for part in error["loc"]), "message": error["msg"]} for error in exc.errors()
    ]
    logging.debug(f"Request payload validation failed: {details}")
    return jsonify({"error": "Invalid request payload", "details": details}), 400


@app.route("/api/exportDeckFile", methods=["POST"])
async def export_deck_file() -> Tuple[Response, int] | Response:
    try:
        payload = ExportDeckFilePayload.model_validate(request.get_json(silent=True))
    except ValidationError as e:
        return invalid_payload_response(e)

    words_data = payload.words
    language = payload.language
    try:
        if language == "de":
            logging.debug(f"Exporting German Anki deck for the word data {words_data}")
            return common_export_cards_file(
                to_word_data_list(words_data, GermanWordData),
                export_fn=german_anki_generate.export_results_to_anki_deck,
                file_suffix="to_import_german_anki_generated.apkg",
            )
        else:
            logging.debug(f"Exporting English Anki deck for the word data {words_data}")
            return common_export_cards_file(
                to_word_data_list(words_data, EnglishWordData),
                export_fn=english_anki_generate.export_results_to_anki_deck,
                file_suffix="to_import_english_anki_generated.apkg",
            )
    except ValidationError as e:
        return invalid_payload_response(e)


WD = TypeVar("WD", GermanWordData, EnglishWordData)


def to_word_data_list(items: list[dict[str, Any]], model: type[WD]) -> list[WD]:
    return [model.model_validate(item) for item in items]


def common_export_cards_file(
    results: list[WD],
    export_fn: Callable[[list[WD], str], None],
    file_suffix: str,
) -> Response:
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


@app.route("/api/generateWordData", methods=["POST"])
async def generate_word_data() -> Tuple[Response, int] | Response:
    try:
        payload = GenerateWordDataPayload.model_validate(request.get_json(silent=True))
    except ValidationError as e:
        return invalid_payload_response(e)

    language = payload.language
    logging.debug(f"Extracting {language} data for the word {payload.word}")
    data: EnglishWordData | GermanWordData
    if language == "de":
        data = await prepare_data_for_german_word(payload.word, payload.to_word_hints())
    else:
        data = await prepare_data_for_english_word(payload.word, payload.to_word_hints())
    return jsonify(data.model_dump(mode="json"))


@app.route("/", methods=["GET"])
def home() -> str:
    return render_template("index.html")


def open_in_browser(*, url: str, after_seconds: int) -> None:
    threading.Timer(after_seconds, lambda: webbrowser.open_new(url)).start()


def main():
    load_dotenv()
    setup_logging()
    init_llm_provider()
    init_tts_engine()
    init_translator()
    open_in_browser(url="http://127.0.0.1:5000/", after_seconds=1)
    app.run(port=5000)
