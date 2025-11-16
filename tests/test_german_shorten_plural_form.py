from src.german_anki_generate import shorten_german_noun_plural_form_for_anki_card


class TestGermanShortenPluralForm:
    def test_simple_ung(self):
        res = shorten_german_noun_plural_form_for_anki_card("Wohnung", "Wohnungen")
        assert "-en" == res

    def test_common_prefix(self):
        res = shorten_german_noun_plural_form_for_anki_card("Zeugnis", "Zeugnisse")
        assert "-se" == res

    def test_same(self):
        res = shorten_german_noun_plural_form_for_anki_card("Lehrer", "Lehrer")
        assert "=" == res

    def test_umlaut(self):
        res = shorten_german_noun_plural_form_for_anki_card("Apfel", "Äpfel")
        assert "die Äpfel" == res
