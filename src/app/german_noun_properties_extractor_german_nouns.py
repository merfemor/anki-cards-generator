import logging

import german_nouns.lookup

from app.german_noun_properties import GermanNounGenus, GermanNounProperties
from app.german_noun_properties_extractor import GermanNounPropertiesExtractor


class GermanNounsNounPropertiesExtractor(GermanNounPropertiesExtractor):
    def __init__(self) -> None:
        self._nouns = german_nouns.lookup.Nouns()

    def extract(self, word: str) -> GermanNounProperties | None:
        result = self._nouns[word]

        if len(result) == 0:
            logging.info(f"Word {word} detected as noun, but not found in dictionary")
            return None

        flexion = result[0]["flexion"]
        genus = GermanNounGenus(result[0].get("genus", "pl"))
        if "nominativ plural" in flexion:
            plural = flexion["nominativ plural"]
        else:
            plural = flexion.get("nominativ plural 1", "")

        return GermanNounProperties(
            singular_form=flexion.get("nominativ singular", ""),
            plural_form=plural,
            genus=genus,
        )
