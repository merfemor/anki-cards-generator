#!/usr/bin/env python3

import logging
import sys

from src.anki_generate import export_results_to_anki_deck
from src.german_data_extract import prepare_data_for_german_word


def read_german_words_from_file(file_path: str) -> [str]:
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read().splitlines()
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <path_to_text_file>")
        sys.exit(1)

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )
    logging.getLogger("httpx").setLevel(logging.CRITICAL)

    file_path = sys.argv[1]

    print(f"Reading words from {file_path}...")
    words = read_german_words_from_file(file_path)
    print(f"File {file_path} was read successfully. Detected {len(words)} word(-s).")

    print("Generating cards data...")
    results = []
    for word in words:
        logging.info(f"Processing word \"{word}\"")
        result = prepare_data_for_german_word(word)
        results.append(result)
        logging.info(f"Processed word \"{word}\", result={result}")

    print("Cards data was successfully generated")
    print("Generating Anki cards...")

    deck_filename = "to_import_anki_generated.apkg"
    export_results_to_anki_deck(results, deck_filename)
    print(f"Successfully saved Anki cards into {deck_filename}")


if __name__ == "__main__":
    main()
