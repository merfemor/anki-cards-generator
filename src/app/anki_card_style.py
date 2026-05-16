# language=css
import textwrap
from typing import Final

ANKI_CARD_CSS: Final[str] = textwrap.dedent("""
    .card {
        font-family: arial;
        font-size: 20px;
        text-align: center;
    }
    .sentence {
       font-size: 15px;
    }
""").strip()
