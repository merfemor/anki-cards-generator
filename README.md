# Anki Cards Generator

Generator of Anki cards for learning German or English words.
Each card contains not only a translation to Russian (and English, in the case of German), but also a sentence example.
Also, audios are generated using text-to-speech and embedded into the cards.

## Installation

**Prerequisites**:

* Python 3.11
* [uv](https://docs.astral.sh/uv/getting-started/installation/)
* [Ollama](https://ollama.com/download) or OpenAI API key
* macOS (text to speech relies on the default `say` command)
* [lame](https://lame.sourceforge.io/)
* [DeepL](https://www.deepl.com/) API key

### LLM provider

You have two options: Ollama (default) and OpenAI.

#### Ollama
 
Download `qwen3.5:4b` model:

```bash
ollama pull qwen3.5:4b
```

#### OpenAI

Set API key into environment variable `OPENAI_API_KEY`:

```bash
export OPENAI_API_KEY=yourkey
```

> [!TIP]
> You can create `.env` file and specify environment variable there to not enter it each time.

Then, when running app, specify additional argument `--llm-provider=openai`.

### DeepL API key

Obtain a DeepL API key as described in [documentation](https://support.deepl.com/hc/en-us/articles/360020695820-API-key-for-DeepL-API#h_01HM9MFQ195GTHM93RRY63M18W).

Write it into environment variable `DEEPL_API_KEY` or `.env` file:

```bash
export DEEPL_API_KEY=key
```

### Python virtual environment

Run the following command to prepare the environment:

```bash
uv sync
```

## Run

Run the app with the following command:

```bash
uv run -m app
```

or just script `run.sh`.

The web interface will be available at http://127.0.0.1:5000/.

When you're done, press `Ctrl+C` to stop the app.

## Development

### Pre-commit hooks

Install pre-commit hooks:

```bash
pre-commit install
```

To run all pre-commit hooks on all files:

```bash
pre-commit run -a
```

### Tests

To run unit tests, execute:

```bash
uv run pytest
```
