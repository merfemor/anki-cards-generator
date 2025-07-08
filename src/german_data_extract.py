from dataclasses import dataclass
from enum import Enum
from typing import Final, Optional

import german_nouns.lookup
from HanTa.HanoverTagger import HanoverTagger

from src.common_data_extract import generate_sentence_example_with_llm
from src.translate import translate_text
from src.utils import check

_german_nouns_obj: Final[german_nouns.lookup.Nouns] = german_nouns.lookup.Nouns()


class PartOfSpeech(Enum):
    Noun = "noun"
    Verb = "verb"
    Other = "other"


def get_pos_tag_of_german_word(de_word: str) -> str:
    tagger_de = HanoverTagger('morphmodel_ger.pgz')
    res = tagger_de.tag_word(de_word)
    return res[0][0]


def pos_tag_to_part_of_speech(pos_tag: str) -> PartOfSpeech:
    if pos_tag == "NN" or pos_tag == "NNI":
        return PartOfSpeech.Noun
    if pos_tag.startswith("VV"):
        return PartOfSpeech.Verb
    return PartOfSpeech.Other


def get_extra_noun_info(word: str) -> (str, str):
    result = _german_nouns_obj[word]

    if len(result) == 0:
        raise NotImplementedError(f"No noun info for word \"{word}\"")

    flexion = result[0]["flexion"]
    genus = result[0].get('genus', "pl")

    if "nominativ plural" in flexion:
        plural = flexion["nominativ plural"]
    else:
        plural = flexion.get("nominativ plural 1", "")

    return flexion.get("nominativ singular", ""), plural, genus


def get_article_for_german_genus(genus: str) -> str:
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


def add_to_to_en_verb(translated_text: str, part_of_speech: PartOfSpeech) -> str:
    if part_of_speech != PartOfSpeech.Verb:
        return translated_text
    if " " in translated_text:
        return translated_text
    return "to " + translated_text


@dataclass
class GermanNounProperties:
    singular_form: str
    plural_form: str
    genus: str
    article: str


@dataclass
class GermanWordData:
    original_word: str
    pos_tag: str
    part_of_speech: PartOfSpeech
    translated_en: str
    translated_ru: str
    noun_properties: Optional[GermanNounProperties]
    sentence_example: str
    sentence_example_translated_en: str


def prepare_data_for_german_word(word: str, stub_ai: bool = False) -> GermanWordData:
    check(len(word.strip()) > 0, f"Expected non empty word")

    pos_tag = get_pos_tag_of_german_word(word)
    check(pos_tag not in ["XY", "$,", "$.", "$("], f"Non word: {word}, pos_tag={pos_tag}")

    part_of_speech = pos_tag_to_part_of_speech(pos_tag)

    translated_en = add_to_to_en_verb(translate_text(word, src="de", dest="en").lower(), part_of_speech)
    translated_ru = translate_text(word, src="de", dest="ru").lower()

    noun_properties = None
    if part_of_speech == PartOfSpeech.Noun:
        singular, plural, genus = get_extra_noun_info(word)
        noun_properties = GermanNounProperties(
            singular_form=singular,
            plural_form=plural,
            genus=genus,
            article=get_article_for_german_genus(genus),
        )

    if stub_ai:
        german_sentence_example = "STUB"
    else:
        german_sentence_example = generate_sentence_example_with_llm(word, language="German")
    sentence_example_translated_en = translate_text(german_sentence_example, src="de", dest="en")

    return GermanWordData(
        original_word=word,
        pos_tag=pos_tag,
        part_of_speech=part_of_speech,
        translated_en=translated_en,
        translated_ru=translated_ru,
        noun_properties=noun_properties,
        sentence_example=german_sentence_example,
        sentence_example_translated_en=sentence_example_translated_en
    )
