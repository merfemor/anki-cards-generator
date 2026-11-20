from abc import ABC, abstractmethod

from app.german_noun_properties import GermanNounProperties


class GermanNounPropertiesExtractor(ABC):
    @abstractmethod
    def extract(self, word: str) -> GermanNounProperties | None:
        raise NotImplementedError
