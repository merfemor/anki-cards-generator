import logging

from app.german_noun_properties import GermanNounProperties
from app.german_noun_properties_extractor import GermanNounPropertiesExtractor


class FallbackGermanNounPropertiesExtractor(GermanNounPropertiesExtractor):
    def __init__(
        self,
        first_extractor: GermanNounPropertiesExtractor,
        second_extractor: GermanNounPropertiesExtractor,
    ) -> None:
        self._extractors = (first_extractor, second_extractor)

    async def extract(self, word: str) -> GermanNounProperties | None:
        for extractor in self._extractors:
            try:
                noun_properties = await extractor.extract(word)
            except Exception:
                logging.exception(
                    "Noun properties extractor %s failed for %s",
                    type(extractor).__name__,
                    word,
                )
                continue

            if noun_properties is not None:
                return noun_properties

        return None
