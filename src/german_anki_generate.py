import logging
import tempfile
import textwrap
from typing import Final

import genanki

from src.tts import german_text_to_speech
from src.utils import check

# Magic constant. Just random number, because we have to assign something unique.
_GENERATED_DECK_ID: Final[int] = 2059400110
_ANKI_MODEL_ID: Final[int] = 1607392319

_GENERATED_DECK_NAME: Final[str] = '[IMPORT OF GENERATED DECK]'
_ANKI_MODEL_NAME: Final[str] = '[TEST] genanki'


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
        <div class="sentence">{{sentence_de}} {{sentence_audio}}</div>
    """).strip()

    CARD_2_ANSWER = textwrap.dedent("""
        {{FrontSide}} <br/>
        {{word_de_article}} {{word_de}} {{word_audio}}
        <hr/>
        <div class="sentence">{{sentence_translated}} {{sentence_audio}}</div>
    """).strip()

    return genanki.Model(
        model_id,
        model_name,
        fields=[
            {'name': 'word_de'},
            {'name': 'word_de_article'},
            {'name': 'word_translated'},
            {'name': 'sentence_de'},
            {'name': 'sentence_translated'},
            {'name': 'word_audio'},
            {'name': 'sentence_audio'},
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '{{word_de_article}} {{word_de}} {{word_audio}}',
                'afmt': CARD_1_ANSWER,
            },
            {
                'name': 'Card 2',
                'qfmt': '{{word_translated}}',
                'afmt': CARD_2_ANSWER,
            }
        ],
        css=CSS)


def _create_anki_note(model: genanki.Model, word_de: str, word_de_article: str, word_translated: str, sentence_de: str,
                      sentence_translated: str, word_audio: str, sentence_audio: str) -> genanki.Note:
    check("/" not in word_audio, f"Audio must be a simple file name, not a path, but got word audio={word_audio}")
    check("/" not in sentence_audio,
          f"Audio must be a simple file name, not a path, but got sentence audio={word_audio}")

    word_audio = f"[sound:{word_audio}]"
    sentence_audio = f"[sound:{sentence_audio}]"
    return genanki.Note(
        model=model,
        fields=[word_de, word_de_article, word_translated, sentence_de, sentence_translated, word_audio,
                sentence_audio])


def export_results_to_anki_deck(results: [dict], deck_filename: str, deck_name: str = _GENERATED_DECK_NAME):
    check(deck_filename.endswith(".apkg"), f"Expected deck filename to have .apkg extension, but got {deck_filename}")

    my_model = _get_anki_card_model()
    my_deck = genanki.Deck(_GENERATED_DECK_ID, deck_name)

    all_media_files = []

    with tempfile.TemporaryDirectory(prefix="anki_cards_generator_media_") as temp_dir:
        logging.info("Created temporary directory " + temp_dir)
        for r in results:
            original_word = r["original_word"]
            word_translated = f"{r["translated_ru"]}, {r["translated_en"]}"

            word_audio_name = f"__anki_generate_{original_word}_word.mp3"
            word_audio_path = f"{temp_dir}/{word_audio_name}"
            sentence_audio_name = f"__anki_generate_{original_word}_sentence.mp3"
            sentence_audio_path = f"{temp_dir}/{sentence_audio_name}"
            german_text_to_speech(r["sentence_example_de"], save_to_path=sentence_audio_path)

            if "noun_properties" in r:
                noun_props = r["noun_properties"]

                if not noun_props["plural_form"]:
                    word_de_for_card = f"{original_word} (Sg.)"
                    word_for_tts = original_word
                elif not noun_props["singular_form"]:
                    word_de_for_card = f"{original_word} (Pl.)"
                    word_for_tts = original_word
                else:
                    word_de_for_card = f"{original_word}, die {noun_props["plural_form"]}"
                    word_for_tts = word_de_for_card

                article = noun_props["article"]
                german_text_to_speech(f"{article} {word_for_tts}", word_audio_path)
                note = _create_anki_note(my_model, word_de=word_de_for_card, word_de_article=article,
                                         word_translated=word_translated,
                                         sentence_de=r["sentence_example_de"],
                                         sentence_translated=r["sentence_example_translated_en"],
                                         word_audio=word_audio_name, sentence_audio=sentence_audio_name)
            else:  # not noun
                german_text_to_speech(original_word, word_audio_path)
                note = _create_anki_note(my_model, word_de=original_word, word_de_article="",
                                         word_translated=word_translated,
                                         sentence_de=r["sentence_example_de"],
                                         sentence_translated=r["sentence_example_translated_en"],
                                         word_audio=word_audio_name, sentence_audio=sentence_audio_name)

            all_media_files.append(word_audio_path)
            all_media_files.append(sentence_audio_path)
            my_deck.add_note(note)

        pkg = genanki.Package(my_deck)
        pkg.media_files = all_media_files
        pkg.write_to_file(deck_filename)
