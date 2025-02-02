# Anki German cards generator

This is a script to generate Anki cards for learning German words using Google Translate and a pinch of AI.
Each card contains not only translation to English and Russian, but also sentence example with translation to English.
Also, audios are generated using text-to-speech and embedded into the cards.

## Installation

### Ollama

Ollama with `cas/discolm-mfto-german` model should be installed.

### Python virtual environment

Create Python virtual environment and install dependencies as follows:

```bash
python3 -m venv .venv

# Activate venv
source .venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

#### Note about `german-nouns` package

I'm constantly getting errors during installation of `german-nouns==1.2.5` package.
This is because of transitive dependency on old `lxml==4.9.4` via `wiktionary-de-parser`.

In order to fix this, install the fresh version of `wiktionary-de-parser` using `pip install wiktionary-de-parser`.
Then, ignore dependencies while installing `german-nouns` using `pip install --no-deps german-nouns`.
This is how we fix stuff here.

## Usage

First, make sure Ollama is running.

Then run script as follows:

```commandline
python main.py file_with_german_words.txt
```

The file is a list of newline-separated **single** German words (without articles).
For example:

```text
Schule
laufen
Markt
jedoch
entweder
groß
```

Finally, import resulting file in Anki.
