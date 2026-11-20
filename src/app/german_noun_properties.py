from enum import Enum
from typing import Literal

from pydantic import BaseModel, model_validator

from app.utils import check


class GermanNounGenus(str, Enum):
    Masculine = "m"
    Neuter = "n"
    Feminine = "f"
    Plural = "pl"


class GermanNounProperties(BaseModel):
    singular_form: str
    plural_form: str
    genus: GermanNounGenus

    @property
    def article(self) -> Literal["der", "die", "das"]:
        match self.genus:
            case GermanNounGenus.Masculine:
                return "der"
            case GermanNounGenus.Neuter:
                return "das"
            case GermanNounGenus.Feminine | GermanNounGenus.Plural:
                return "die"

    @model_validator(mode="after")
    def check_forms(self) -> "GermanNounProperties":
        check(
            self.singular_form != "" or self.plural_form != "", "Either singular_form or plural_form must be not empty"
        )
        return self
