import logging
import tempfile
import textwrap
from typing import Final

import genanki

from src.tts import text_to_speech_into_file
from src.utils import check

# Magic constant. Just random number, because we have to assign something unique.
_GENERATED_DECK_ID: Final[int] = 2059400111
_ANKI_MODEL_ID: Final[int] = 1607392320

_GENERATED_DECK_NAME: Final[str] = '[Anki Cards Generator] – GENERATED ENGLISH'
_ANKI_MODEL_NAME: Final[str] = '[Anki Cards Generator] Basic With Sentence'


def _get_anki_card_model(model_id: int = _ANKI_MODEL_ID, model_name: str = _ANKI_MODEL_NAME) -> genanki.Model:
    CSS = textwrap.dedent("""
        .card {
            font-family: arial;
            font-size: 20px;
            text-align: center;
        }
        .sentence {
	       font-size: 15px;
        }
    """).strip()

    CARD_1_ANSWER = textwrap.dedent("""
        {{FrontSide}} <br/>
        {{word_translated}}
        <hr/>
        <div class="sentence">{{sentence}} {{sentence_audio}}</div>
    """).strip()

    CARD_2_ANSWER = textwrap.dedent("""
        {{FrontSide}} <br/>
        {{word}} {{word_audio}}
        <hr/>
        <div class="sentence">{{sentence_translated}} {{sentence_audio}}</div>
    """).strip()

    return genanki.Model(
        model_id,
        model_name,
        fields=[
            {'name': 'word'},
            {'name': 'word_translated'},
            {'name': 'sentence'},
            {'name': 'sentence_translated'},
            {'name': 'word_audio'},
            {'name': 'sentence_audio'},
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '{{word}} {{word_audio}}',
                'afmt': CARD_1_ANSWER,
            },
            {
                'name': 'Card 2',
                'qfmt': '{{word_translated}}',
                'afmt': CARD_2_ANSWER,
            }
        ],
        css=CSS)


def _create_anki_note(model: genanki.Model, word: str, word_translated: str, sentence: str,
                      sentence_translated: str, word_audio: str, sentence_audio: str) -> genanki.Note:
    check("/" not in word_audio, f"Audio must be a simple file name, not a path, but got word audio={word_audio}")
    check("/" not in sentence_audio,
          f"Audio must be a simple file name, not a path, but got sentence audio={word_audio}")

    word_audio = f"[sound:{word_audio}]"
    sentence_audio = f"[sound:{sentence_audio}]"
    return genanki.Note(
        model=model,
        fields=[word, word_translated, sentence, sentence_translated, word_audio, sentence_audio])


def export_results_to_anki_deck(results: [dict[str, str]], deck_filename: str, deck_name: str = _GENERATED_DECK_NAME):
    check(deck_filename.endswith(".apkg"), f"Expected deck filename to have .apkg extension, but got {deck_filename}")

    my_model = _get_anki_card_model()
    my_deck = genanki.Deck(_GENERATED_DECK_ID, deck_name)

    all_media_files = []

    with tempfile.TemporaryDirectory(prefix="anki_cards_generator_media_") as temp_dir:
        logging.info("Created temporary directory " + temp_dir)
        for r in results:
            original_word = r["original_word"]

            word_audio_name = f"anki_cards_generator_en_{original_word}_word.mp3"
            word_audio_path = f"{temp_dir}/{word_audio_name}"
            text_to_speech_into_file(original_word, word_audio_path, lang="en")
            all_media_files.append(word_audio_path)

            sentence_audio_name = f"anki_cards_generator_en_{original_word}_sentence.mp3"
            sentence_audio_path = f"{temp_dir}/{sentence_audio_name}"
            text_to_speech_into_file(r["sentence_example_en"], sentence_audio_path, lang="en")
            all_media_files.append(sentence_audio_path)

            note = _create_anki_note(my_model, word=original_word,
                                     word_translated=r["translated_ru"],
                                     sentence=r["sentence_example_en"],
                                     sentence_translated=r["sentence_example_translated_ru"],
                                     word_audio=word_audio_name, sentence_audio=sentence_audio_name)
            my_deck.add_note(note)

        pkg = genanki.Package(my_deck)
        pkg.media_files = all_media_files
        pkg.write_to_file(deck_filename)
