import asyncio
import json
import logging
from typing import Final
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import Request, urlopen

from pydantic import BaseModel, Field

from app.german_noun_properties import GermanNounGenus, GermanNounProperties
from app.german_noun_properties_extractor import GermanNounPropertiesExtractor

_WIKTAPI_BASE_URL: Final[str] = "https://api.wiktapi.dev"
_REQUEST_TIMEOUT_SECONDS: Final[float] = 5.0
_WIKTAPI_NOT_FOUND: Final[object] = object()
_ARTICLES_TO_GENUS: Final[dict[str, GermanNounGenus]] = {
    "der": GermanNounGenus.Masculine,
    "das": GermanNounGenus.Neuter,
    "die": GermanNounGenus.Feminine,
}


class _WiktApiForm(BaseModel):
    form: str
    tags: list[str]
    article: str | None = None


class _WiktApiPartOfSpeechForms(BaseModel):
    pos: str
    lang_code: str
    forms: list[_WiktApiForm]


class _WiktApiFormsResponse(BaseModel):
    forms: list[_WiktApiPartOfSpeechForms]


class _WiktApiFormOf(BaseModel):
    word: str


class _WiktApiSense(BaseModel):
    tags: list[str] = Field(default_factory=list)
    form_of: list[_WiktApiFormOf] = Field(default_factory=list)


class _WiktApiEntry(BaseModel):
    senses: list[_WiktApiSense] = Field(default_factory=list)


class _WiktApiWordResponse(BaseModel):
    entries: list[_WiktApiEntry]


def _fetch_forms_payload(url: str) -> object:
    request = Request(url, headers={"Accept": "application/json", "User-Agent": "anki-cards-generator/0.1.0"})
    with urlopen(request, timeout=_REQUEST_TIMEOUT_SECONDS) as response:
        return json.load(response)


class WiktApiGermanNounPropertiesExtractor(GermanNounPropertiesExtractor):
    async def extract(self, word: str) -> GermanNounProperties | None:
        response_payload = await self._fetch_payload(self._forms_url(word))
        if response_payload is _WIKTAPI_NOT_FOUND:
            logging.info(f"Word {word} not found in WiktAPI")
            return None

        noun_properties = self._parse_forms(response_payload)
        if noun_properties is not None:
            return noun_properties

        lemma = await self._get_lemma(word)
        if lemma is None:
            logging.info(f"Word {word} detected as noun, but not found in WiktAPI")
            return None

        lemma_response_payload = await self._fetch_payload(self._forms_url(lemma))
        if lemma_response_payload is _WIKTAPI_NOT_FOUND:
            raise ValueError(f"WiktAPI returned lemma {lemma} for {word}, but no forms entry for {lemma}")

        return self._parse_forms(lemma_response_payload)

    @staticmethod
    def _forms_url(word: str) -> str:
        encoded_word = quote(word, safe="")
        return f"{_WIKTAPI_BASE_URL}/v1/de/word/{encoded_word}/forms?lang=de"

    @staticmethod
    async def _fetch_payload(url: str) -> object:
        try:
            return await asyncio.to_thread(_fetch_forms_payload, url)
        except HTTPError as error:
            if error.code == 404:
                return _WIKTAPI_NOT_FOUND
            raise

    async def _get_lemma(self, word: str) -> str | None:
        encoded_word = quote(word, safe="")
        url = f"{_WIKTAPI_BASE_URL}/v1/de/word/{encoded_word}?lang=de"
        response_payload = await self._fetch_payload(url)
        if response_payload is _WIKTAPI_NOT_FOUND:
            return None

        payload = _WiktApiWordResponse.model_validate(response_payload)
        for entry in payload.entries:
            for sense in entry.senses:
                if "form-of" not in sense.tags:
                    continue
                for form_of in sense.form_of:
                    return form_of.word
        return None

    @staticmethod
    def _parse_forms(response_payload: object) -> GermanNounProperties | None:
        payload = _WiktApiFormsResponse.model_validate(response_payload)
        for part_of_speech in payload.forms:
            if part_of_speech.pos != "noun" or part_of_speech.lang_code != "de":
                continue

            singular_form = ""
            for form in part_of_speech.forms:
                if "nominative" in form.tags and "singular" in form.tags:
                    singular_form = form.form
                    break

            plural_form = ""
            for form in part_of_speech.forms:
                if "nominative" in form.tags and "plural" in form.tags:
                    plural_form = form.form
                    break

            if singular_form:
                article = None
                for form in part_of_speech.forms:
                    if "nominative" in form.tags and "singular" in form.tags and form.article in _ARTICLES_TO_GENUS:
                        article = form.article
                        break
                if article is None:
                    continue
                genus = _ARTICLES_TO_GENUS[article]
            elif plural_form:
                genus = GermanNounGenus.Plural
            else:
                continue

            return GermanNounProperties(
                singular_form=singular_form,
                plural_form=plural_form,
                genus=genus,
            )

        return None
