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

Ollama with `llama3.1:8b` model should be installed.

```bash
ollama pull llama3.1:8b
```

Then, when running server.py, specify additional argument `--llm-provider=ollama`.

### Python virtual environment

Install [Poetry](https://python-poetry.org/docs/#installation).

Make sure that `virtualenvs.in-project` is set to `true`:

```bash
poetry config virtualenvs.in-project

# If not, set it to true
poetry config virtualenvs.in-project true --local
```

```bash
# Install dependencies
poetry install

# Activate env
eval $(poetry env activate)

# Hack to resolve dependency conflict (see below)
pip install --no-deps german-nouns
```

#### Note about `german-nouns` package

I'm constantly getting errors during installation of `german-nouns==1.2.5` package.
This is because of transitive dependency on old `lxml==4.9.4` via `wiktionary-de-parser`.
That's why we have to install `german-nouns` separately with ignoring dependencies.
This is how we fix stuff here.

## Usage

### Server

* In the case of Ollama provider, make sure it is up and running.
* In the case of OpenAI, provide API key through environment variable:

```bash
export OPENAI_API_KEY=yourkey
```

> [!TIP]
> You can create `.env` file and specify environment variable there to not enter it each time.

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

## Development

Install pre-commit hooks:

```bash
pre-commit install
```

## Tests

To run unit tests, execute:

```bash
python -m unittest tests/*.py
```
