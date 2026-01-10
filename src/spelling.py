from spellchecker import SpellChecker

from utils import check

_spells = {
    "en": SpellChecker(language="en"),
    "de": SpellChecker(language="de"),
}


def correct_spelling(word_or_phrase: str, language: str) -> str:
    check(len(word_or_phrase) > 0, "Expected non empty string")

    if " " in word_or_phrase:
        # No spell checking for phrases for now
        return word_or_phrase

    spell = _spells.get(language)
    orig = word_or_phrase
    corrected = spell.correction(word_or_phrase)
    if not corrected:
        return orig

    # Spell checker doesn't preserve a word case, we have to restore it
    if orig.islower():
        return corrected.lower()
    else:
        return corrected.capitalize()
