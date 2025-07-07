import logging
import os
import sys
import tempfile

from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS

import src.english_anki_generate
import src.german_anki_generate
from src.configuration import parse_arguments, set_global_llm_provider
from src.english_data_extract import prepare_data_for_english_word
from src.german_data_extract import prepare_data_for_german_word

app = Flask(__name__)
CORS(app, origins=["http://127.0.0.1:8000", "http://localhost:8000"])


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )
    logging.getLogger("httpx").setLevel(logging.CRITICAL)


@app.route('/api/generateCardsFile', methods=['POST'])
def generate_german_cards_file():
    words = request.get_json().get('words', [])
    if not words:
        return jsonify({'error': 'The "words" list cannot be empty'}), 400

    language = request.get_json().get('language')

    if language == 'de':
        prepare_data_fn = prepare_data_for_german_word
        export_fn = src.german_anki_generate.export_results_to_anki_deck
        file_suffix = "to_import_german_anki_generated.apkg"
    elif language == 'en':
        prepare_data_fn = prepare_data_for_english_word
        export_fn = src.english_anki_generate.export_results_to_anki_deck
        file_suffix = "to_import_english_anki_generated.apkg"
    else:
        return jsonify({'error': f"Expected language to be one of 'en', 'de', but got '{language}'"}), 400

    logging.info(f"Preparing card data for language {language} for the words {words}")
    results = []
    for word in words:
        result = prepare_data_fn(word)
        results.append(result)

    with tempfile.NamedTemporaryFile(delete=False, suffix=file_suffix) as temp_file:
        deck_filename = temp_file.name

    logging.info(f"Exporting the results into the temporary Anki deck file \"{deck_filename}\"")
    try:
        export_fn(results, deck_filename)

        response = send_file(deck_filename, as_attachment=True, download_name=os.path.basename(deck_filename),
                             mimetype='application/octet-stream')
        return response
    finally:
        if os.path.exists(deck_filename):
            os.remove(deck_filename)
            logging.info(f"Removed temporary Anki deck file \"{deck_filename}\"")


if __name__ == '__main__':
    load_dotenv()
    setup_logging()
    args = parse_arguments()
    set_global_llm_provider(args.llm_provider)
    app.run(port=5000)
