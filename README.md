# Anki Cards Generator

Generator of Anki cards for learning German or English words using Google Translate and a pinch of AI.
Each card contains not only translation to Russian (and English in case of German), but also a sentence example with a translation to English or Russian.
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

### Script for German words

First, make sure Ollama is running.

Then run script as follows:

```commandline
python main_de.py file_with_german_words.txt
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

### Script for English words

First, make sure Ollama is running.

Then run script as follows:

```commandline
python main_en.py file_with_english_words.txt
```
The file is a list of newline-separated English words.
For example:

```text
resemblance
to put up with
condescending
```

Finally, import resulting file in Anki.

### Server mode

There is also an HTTP server mode.

It can be run with the following command:

```bash
python server.py
```

Press `Ctrl+C` to stop the server.

Currently available endpoints are:

1. `GET /api/generateGermanCard?word=Sprache`
2. `GET /api/generateEnglishCard?word=language`

Beware that the response time is very long, far from instant.

### Web interface

Also, there is a web interface. See more in separate [README](./website/README.md).
