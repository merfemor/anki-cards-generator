from typing import Annotated

from pydantic import BaseModel, StringConstraints

from app.word_hints import WordHints


class WordHintsPayload(BaseModel):
    translated_ru: Annotated[str, StringConstraints(strip_whitespace=True)] = ""


class WordPayload(BaseModel):
    word: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    hints: WordHintsPayload | None = None

    def to_word_hints(self) -> WordHints:
        if self.hints is None:
            return WordHints(translated_ru="")
        return WordHints(translated_ru=self.hints.translated_ru)


class GenerateCardsFilePayload(BaseModel):
    language: str
    words: list[WordPayload] = []
