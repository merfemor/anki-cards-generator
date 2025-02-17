#!/usr/bin/env python3

import logging
import sys

from src.english_anki_generate import export_results_to_anki_deck
from src.english_data_extract import prepare_data_for_english_word
from src.utils import read_words_file


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )
    logging.getLogger("httpx").setLevel(logging.CRITICAL)


def main():
    if len(sys.argv) != 2:
        print("Usage: python main_en.py <path_to_text_file>")
        sys.exit(1)

    setup_logging()

    file_path = sys.argv[1]

    print(f"Reading words from {file_path}...")
    words = read_words_file(file_path)
    print(f"File {file_path} was read successfully. Detected {len(words)} word(-s).")

    print("Generating cards data...")
    results = []
    for word in words:
        logging.info(f"Processing word \"{word}\"")
        result = prepare_data_for_english_word(word)
        results.append(result)
        logging.info(f"Processed word \"{word}\", result={result}")

    print("Cards data was successfully generated")
    print("Generating Anki cards...")

    deck_filename = "to_import_english_anki_generated.apkg"
    export_results_to_anki_deck(results, deck_filename)
    print(f"Successfully saved Anki cards into {deck_filename}")


if __name__ == "__main__":
    main()
