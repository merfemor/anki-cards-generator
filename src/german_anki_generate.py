import logging
import tempfile
import textwrap
from typing import Final

import genanki
from genanki import Note

from src.anki_card_style import ANKI_CARD_CSS
from src.anki_common import get_audio_file_name_for_phrase, get_audio_file_name_for_sentence
from src.german_data_extract import GermanWordData
from src.tts import text_to_speech_into_file
from src.utils import check

# Magic constant. Just random number, because we have to assign something unique.
_GENERATED_DECK_ID: Final[int] = 2059400110
_ANKI_MODEL_ID: Final[int] = 1607392319

_GENERATED_DECK_NAME: Final[str] = "[Anki Cards Generator] – GENERATED GERMAN"
_ANKI_MODEL_NAME: Final[str] = "[Anki Cards Generator] German with Sentence and Article"


def _get_anki_card_model(model_id: int = _ANKI_MODEL_ID, model_name: str = _ANKI_MODEL_NAME) -> genanki.Model:
    # language=html
    CARD_1_ANSWER = textwrap.dedent("""
        {{FrontSide}} <br/>
        {{word_translated}}
        <hr/>
        <div class="sentence">{{sentence_de}} {{sentence_audio}}</div>
    """).strip()

    # language=html
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
            {"name": "word_de"},
            {"name": "word_de_article"},
            {"name": "word_translated"},
            {"name": "sentence_de"},
            {"name": "sentence_translated"},
            {"name": "word_audio"},
            {"name": "sentence_audio"},
        ],
        templates=[
            {
                "name": "Card 1",
                "qfmt": "{{word_de_article}} {{word_de}} {{word_audio}}",
                "afmt": CARD_1_ANSWER,
            },
            {
                "name": "Card 2",
                "qfmt": "{{word_translated}}",
                "afmt": CARD_2_ANSWER,
            },
        ],
        css=ANKI_CARD_CSS,
    )


def _create_anki_note(
    model: genanki.Model,
    word_de: str,
    word_de_article: str,
    word_translated: str,
    sentence_de: str,
    sentence_translated: str,
    word_audio: str,
    sentence_audio: str,
) -> genanki.Note:
    check("/" not in word_audio, f"Audio must be a simple file name, not a path, but got word audio={word_audio}")
    check(
        "/" not in sentence_audio, f"Audio must be a simple file name, not a path, but got sentence audio={word_audio}"
    )

    word_audio = f"[sound:{word_audio}]"
    sentence_audio = f"[sound:{sentence_audio}]"
    return genanki.Note(
        model=model,
        fields=[
            word_de,
            word_de_article,
            word_translated,
            sentence_de,
            sentence_translated,
            word_audio,
            sentence_audio,
        ],
    )


def shorten_german_noun_plural_form_for_anki_card(word_singular: str, word_plural: str) -> str:
    """
    Shortens plural noun form if possible.
    This is needed to not write the full form in simple cases, e.g.:
    * "die Wohnung, -en" instead of "die Wohnung, die Wohnungen".
    * "der Lehrer, =" instead of "der Lehrer, die Lehrer"

    More complex cases with umlauts are not handled, e.g.:
    * "die Stadt, die Städte", but could be "die Stadt, –ä, e"
    * "die Mutter, die Mütter", but could be "die Mutter, -ü"
    """
    if word_singular == word_plural:
        return "="
    elif word_plural.startswith(word_singular):
        return "-" + word_plural[len(word_singular) :]
    else:
        return "die " + word_plural


def export_results_to_anki_deck(
    results: list[GermanWordData], deck_filename: str, deck_name: str = _GENERATED_DECK_NAME
) -> None:
    check(deck_filename.endswith(".apkg"), f"Expected deck filename to have .apkg extension, but got {deck_filename}")

    my_model = _get_anki_card_model()
    my_deck = genanki.Deck(_GENERATED_DECK_ID, deck_name)

    all_media_files: list[str] = []

    with tempfile.TemporaryDirectory(prefix="anki_cards_generator_media_") as temp_dir:
        logging.info("Created temporary directory " + temp_dir)
        for r in results:
            note = _create_anki_note_for_german_word_data(r, my_model, all_media_files, temp_dir)
            my_deck.add_note(note)

        pkg = genanki.Package(my_deck)
        pkg.media_files = all_media_files
        pkg.write_to_file(deck_filename)


def _create_anki_note_for_german_word_data(
    r: GermanWordData, model: genanki.Model, all_media_files: list[str], temp_dir: str
) -> Note:
    word_translated = f"{r.translated_ru}, {r.translated_en}"
    word_de_for_card = r.word_infinitive
    word_audio_text = r.word_infinitive
    word_article = ""
    word_audio_name = get_audio_file_name_for_phrase(r.word_infinitive, lang="de")
    word_audio_path = f"{temp_dir}/{word_audio_name}"
    sentence_audio_name = get_audio_file_name_for_sentence(r.word_infinitive, lang="de")
    sentence_audio_path = f"{temp_dir}/{sentence_audio_name}"
    text_to_speech_into_file(r.sentence_example, sentence_audio_path, lang="de")
    if r.noun_properties:
        noun_props = r.noun_properties

        if not noun_props.plural_form:
            word_de_for_card = f"{r.word_infinitive} (Sg.)"
        elif not noun_props.singular_form:
            word_de_for_card = f"{r.word_infinitive} (Pl.)"
        else:
            shortened_plural_form = shorten_german_noun_plural_form_for_anki_card(
                noun_props.singular_form, noun_props.plural_form
            )
            word_de_for_card = f"{r.word_infinitive}, {shortened_plural_form}"

        word_article = noun_props.article
        word_audio_text = f"{noun_props.article} {r.word_infinitive}"
    text_to_speech_into_file(word_audio_text, word_audio_path, lang="de")
    note = _create_anki_note(
        model,
        word_de=word_de_for_card,
        word_de_article=word_article,
        word_translated=word_translated,
        sentence_de=r.sentence_example,
        sentence_translated=r.sentence_example_translated_en,
        word_audio=word_audio_name,
        sentence_audio=sentence_audio_name,
    )
    all_media_files.append(word_audio_path)
    all_media_files.append(sentence_audio_path)
    return note
