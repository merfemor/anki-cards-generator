import os
import tempfile
from typing import Callable

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS

import src.english_anki_generate
import src.german_anki_generate
from src.english_data_extract import prepare_data_for_english_word
from src.german_data_extract import prepare_data_for_german_word

app = Flask(__name__)
CORS(app, origins=["http://127.0.0.1:8000", "http://localhost:8000"])


def generate_cards_file_common[R](words: list[str], prepare_data_fn: Callable[[str], R],
                                  export_fn: Callable[[list[R], str], None], file_suffix: str):
    if not words:
        return jsonify({'error': 'The "words" list cannot be empty'}), 400

    results = []
    for word in words:
        result = prepare_data_fn(word)  # Use the language-specific data preparation function
        results.append(result)

    # Generate a unique temporary file name for the deck
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_suffix) as temp_file:
        deck_filename = temp_file.name

    # Export the results to the temporary file
    try:
        export_fn(results, deck_filename)  # Use the language-specific export function

        # Send the file to the client
        response = send_file(deck_filename, as_attachment=True, download_name=os.path.basename(deck_filename),
                             mimetype='application/octet-stream')
        return response
    finally:
        # Ensure cleanup in case of an exception
        if os.path.exists(deck_filename):
            os.remove(deck_filename)


@app.route('/api/generateGermanCardsFile', methods=['POST'])
def generate_german_cards_file():
    words = request.get_json().get('words', [])
    return generate_cards_file_common(
        words,
        prepare_data_fn=prepare_data_for_german_word,
        export_fn=src.german_anki_generate.export_results_to_anki_deck,
        file_suffix="to_import_german_anki_generated.apkg"
    )


@app.route('/api/generateEnglishCardsFile', methods=['POST'])
def generate_english_cards_file():
    words = request.get_json().get('words', [])
    return generate_cards_file_common(
        words,
        prepare_data_fn=prepare_data_for_english_word,
        export_fn=src.english_anki_generate.export_results_to_anki_deck,
        file_suffix="to_import_english_anki_generated.apkg"
    )


if __name__ == '__main__':
    app.run(port=5000)
