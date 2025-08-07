# Anki Cards Generator

Generator of Anki cards for learning German or English words using Google Translate and a pinch of AI.
Each card contains not only translation to Russian (and English in case of German), but also a sentence example with a translation to English or Russian.
Also, audios are generated using text-to-speech and embedded into the cards.

## Installation

### LLM provider

You have two options: Ollama (default) and OpenAI.

#### Ollama

Install [Ollama](https://ollama.com/download) client and run it. 
 
Pull `llama3.1:8b` model:

```bash
ollama pull llama3.1:8b
```

#### OpenAI

Set API key into environment variable `OPENAI_API_KEY`:

```bash
export OPENAI_API_KEY=yourkey
```

> [!TIP]
> You can create `.env` file and specify environment variable there to not enter it each time.

Then, when running app, specify additional argument `--llm-provider=openai`.

### Python virtual environment

Install [Poetry](https://python-poetry.org/docs/#installation).

Then run the following commands to prepare the environment:

```bash
# Install dependencies
poetry install

# Activate env
source .venv/bin/activate

# Hack to resolve dependency conflict (see below)
pip install --no-deps german-nouns
```

#### Note about `german-nouns` package

I'm constantly getting errors during installation of `german-nouns==1.2.5` package.
This is because of transitive dependency on old `lxml==4.9.4` via `wiktionary-de-parser`.
That's why we have to install `german-nouns` separately with ignoring dependencies.
This is how we fix stuff here.

## Run

Activate virtual environment if haven't yet.

```bash
source .venv/bin/activate
```

Run the app with the following command:

```bash
python main.py
```

The web interface will be available at http://127.0.0.1:5000/.

When you're done, press `Ctrl+C` to stop the app.

## Development

Install pre-commit hooks:

```bash
pre-commit install
```

To run all pre-commit hooks on all files:

```bash
pre-commit run -a
```

## Tests

To run unit tests, execute:

```bash
PYTHONPATH=. poetry run pytest
```
