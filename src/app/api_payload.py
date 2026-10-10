from typing import Annotated, Any, Literal

from pydantic import BaseModel, Field, StringConstraints

from app.word_hints import WordHints

Language = Literal["de", "en"]


class WordHintsPayload(BaseModel):
    translated_ru: Annotated[str, StringConstraints(strip_whitespace=True)] = ""


class GenerateWordDataPayload(BaseModel):
    language: Language
    word: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    hints: WordHintsPayload | None = None

    def to_word_hints(self) -> WordHints:
        if self.hints is None:
            return WordHints(translated_ru="")
        return WordHints(translated_ru=self.hints.translated_ru)


class ExportDeckFilePayload(BaseModel):
    """Word data as it is returned by the /api/generateWordData endpoint."""

    language: Language
    words: list[dict[str, Any]] = Field(min_length=1)
