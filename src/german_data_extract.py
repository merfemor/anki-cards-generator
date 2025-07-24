import logging
from dataclasses import dataclass
from enum import Enum
from typing import Final, Optional, Literal, Tuple

import german_nouns.lookup
from HanTa.HanoverTagger import HanoverTagger

from src.common_data_extract import generate_sentence_example_with_llm
from src.translate import translate_text
from src.utils import check
from src.word_hints import WordHints

_pos_tagger_de = HanoverTagger("morphmodel_ger.pgz")
_german_nouns_obj: Final[german_nouns.lookup.Nouns] = german_nouns.lookup.Nouns()


class PartOfSpeech(Enum):
    Noun = "noun"
    Verb = "verb"
    Other = "other"


def pos_tag_to_part_of_speech(pos_tag: str) -> PartOfSpeech:
    if pos_tag == "NN" or pos_tag == "NNI":
        return PartOfSpeech.Noun
    if pos_tag.startswith("VV"):
        return PartOfSpeech.Verb
    return PartOfSpeech.Other


def get_extra_noun_info(word: str) -> Tuple[str, str, str]:
    result = _german_nouns_obj[word]

    if len(result) == 0:
        raise NotImplementedError(f'No noun info for word "{word}"')

    flexion = result[0]["flexion"]
    genus = result[0].get("genus", "pl")

    if "nominativ plural" in flexion:
        plural = flexion["nominativ plural"]
    else:
        # The case when a word can have two possible plural forms, e.g., das Band
        plural = flexion.get("nominativ plural 1", "")

    return flexion.get("nominativ singular", ""), plural, genus


def get_article_for_german_genus(genus: str) -> Literal["der", "die", "das"]:
    match genus:
        case "m":
            return "der"
        case "n":
            return "das"
        case "f":
            return "die"
        case "pl":
            return "die"
        case _:
            raise ValueError("Unexpected genus: " + genus)


def post_process_en_translation(translated_text: str, part_of_speech: PartOfSpeech) -> str:
    if part_of_speech == PartOfSpeech.Verb:
        if not translated_text.startswith("to "):
            return "to " + translated_text
    elif part_of_speech == PartOfSpeech.Noun:
        if translated_text.startswith("the "):
            return translated_text[4:]
    return translated_text


@dataclass
class GermanNounProperties:
    singular_form: str
    plural_form: str
    genus: str
    article: Literal["der", "die", "das"]

    def __post_init__(self) -> None:
        check(
            self.singular_form != "" or self.plural_form != "", "Either singular_form or plural_form must be not empty"
        )


@dataclass
class GermanWordData:
    word_infinitive: str
    pos_tag: str
    part_of_speech: PartOfSpeech
    translated_en: str
    translated_ru: str
    noun_properties: Optional[GermanNounProperties]
    sentence_example: str
    sentence_example_translated_en: str


def strip_noun_article(word: str) -> str:
    if word.startswith("der ") or word.startswith("die ") or word.startswith("das "):
        return word[4:]
    return word


async def prepare_data_for_german_word(original_word_or_phrase: str, hints: WordHints) -> GermanWordData:
    word_or_phrase = strip_noun_article(original_word_or_phrase)
    check(len(word_or_phrase.strip()) > 0, "Expected non empty word_or_phrase")

    if not is_single_word(word_or_phrase):
        return await prepare_data_for_german_phrase(word_or_phrase, hints)

    word = word_or_phrase

    word_infinitive, pos_tag = _pos_tagger_de.analyze(word)
    check(pos_tag not in ["XY", "$,", "$.", "$("], f"Non word: {word}, pos_tag={pos_tag}")

    part_of_speech = pos_tag_to_part_of_speech(pos_tag)

    if part_of_speech != PartOfSpeech.Noun:
        # For some words infinitives start with capital letter despite they are not nouns, e.g. "perplex"
        word_infinitive = word_infinitive.lower()

    if original_word_or_phrase != word_infinitive:
        logging.info(f"Auto corrected word: original={original_word_or_phrase}, infinitive={word_infinitive}")

    noun_properties = None
    word_infinitive_with_article = word_infinitive

    if part_of_speech == PartOfSpeech.Noun:
        singular, plural, genus = get_extra_noun_info(word_infinitive)
        noun_properties = GermanNounProperties(
            singular_form=singular,
            plural_form=plural,
            genus=genus,
            article=get_article_for_german_genus(genus),
        )
        word_infinitive_with_article = f"{noun_properties.article} {word_infinitive}"

    german_sentence_example = await generate_sentence_example_with_llm(word_infinitive_with_article, language="German")
    sentence_example_translated_en = await translate_text(german_sentence_example, src="de", dest="en")

    return GermanWordData(
        word_infinitive=word_infinitive,
        pos_tag=pos_tag,
        part_of_speech=part_of_speech,
        translated_en=await translate_de_to_en(word_infinitive_with_article, part_of_speech),
        translated_ru=await translate_de_to_ru(word_infinitive_with_article, hints),
        noun_properties=noun_properties,
        sentence_example=german_sentence_example,
        sentence_example_translated_en=sentence_example_translated_en,
    )


async def prepare_data_for_german_phrase(phrase: str, hints: WordHints) -> GermanWordData:
    german_sentence_example = await generate_sentence_example_with_llm(phrase, language="German")

    return GermanWordData(
        word_infinitive=phrase,
        pos_tag="",
        part_of_speech=PartOfSpeech.Other,
        translated_en=await translate_de_to_en(phrase, PartOfSpeech.Other),
        translated_ru=await translate_de_to_ru(phrase, hints),
        noun_properties=None,
        sentence_example=german_sentence_example,
        sentence_example_translated_en=await translate_text(german_sentence_example, src="de", dest="en"),
    )


async def translate_de_to_ru(text: str, hints: WordHints) -> str:
    if hints.translated_ru:
        return hints.translated_ru
    else:
        return (await translate_text(text, src="de", dest="ru")).lower()


async def translate_de_to_en(text: str, part_of_speech: PartOfSpeech) -> str:
    translation = (await translate_text(text, src="de", dest="en")).lower()
    return post_process_en_translation(translation, part_of_speech)


def is_single_word(word_or_phrase: str) -> bool:
    if word_or_phrase.startswith("sich "):
        word_or_phrase = word_or_phrase[5:].strip()
    return " " not in word_or_phrase
