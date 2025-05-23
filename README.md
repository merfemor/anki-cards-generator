# Anki Cards Generator

Generator of Anki cards for learning German or English words using Google Translate and a pinch of AI.
Each card contains not only translation to Russian (and English in case of German), but also a sentence example with a translation to English or Russian.
Also, audios are generated using text-to-speech and embedded into the cards.

## Installation

### LLM provider

You have two options: OpenAI (default) and Ollama.

#### OpenAI

Set key into environment variable `OPENAI_API_KEY`:

```bash
export OPENAI_API_KEY=yourkey
```

#### Ollama

Ollama with `cas/discolm-mfto-german` model should be installed.
Then, when running server.py, specify additional argument `--ai-provider=ollama`.

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

### Server

* In the case of Ollama provider, make sure it is up and running.
* In the case of OpenAI, provide API key through environment variable:

```bash
export OPENAI_API_KEY=yourkey
```

Run the server with the following command:

```bash
python server.py
```

Press `Ctrl+C` to stop the server.

Beware that the response time is very long, far from instant.

### Web interface

Run web interface:

```bash
./website/run.sh
```

For now, it only works on localhost, because endpoint path is hardcoded in JS.
