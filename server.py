import json
from dataclasses import asdict

from flask import Flask, jsonify, request, Response

from src.english_data_extract import prepare_data_for_english_word
from src.german_data_extract import prepare_data_for_german_word

app = Flask(__name__)


@app.route('/api/generateGermanCard', methods=['GET'])
def generate_german_card():
    word = request.args.get('word')
    if not word:  # None or empty
        return jsonify({'error': 'Missing or empty "word" parameter'}), 400

    result = prepare_data_for_german_word(word)
    return Response(
        json.dumps(asdict(result), ensure_ascii=False),
        mimetype='application/json'
    )


@app.route('/api/generateEnglishCard', methods=['GET'])
def generate_english_card():
    word = request.args.get('word')
    if not word:  # None or empty
        return jsonify({'error': 'Missing or empty "word" parameter'}), 400

    result = prepare_data_for_english_word(word)
    return Response(
        json.dumps(asdict(result), ensure_ascii=False),
        mimetype='application/json'
    )


if __name__ == '__main__':
    app.run(debug=True)
