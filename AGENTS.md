# AI Coding Agent Instructions — anki-cards-generator

Python 3.11 project that generates Anki flashcards for learning German/English words, with translations (DeepL), sentence examples (LLM: Ollama or OpenAI), and TTS audio (macOS `say`).

## Tech stack

- Flask (async) web app with a web UI (vanilla JS + Alpine.js, plain CSS, no bundler)
- Gunicorn production WSGI server (`gunicorn.conf.py`)
- `uv` for dependency management
- Ruff (lint + format) + mypy for type checking
- pytest for tests
- Pre-commit hooks configured

## Run

```bash
./run.sh                # start production server with Gunicorn (or: uv run gunicorn 'app.main:prod_entry()')
uv run app-dev          # start web UI in debug mode at :5000
uv run pytest           # run tests
uv run pre-commit run -a       # lint, format, type-check
```

## Code conventions

- Line length: 120 (enforced by Ruff).
- Use type hints on all function signatures.
- Source code lives under `src/app/`, tests under `tests/`.
- Async I/O (LLM calls, translations, TTS) uses `async`/`await`.
- The `main.py` module owns the Flask app and route handlers; business logic is delegated to separate modules (`*_data_extract`, `*_anki_generate`, etc.).
- In `main.py`, `prod_entry()` returns the `Flask` app for Gunicorn; `debug_entry()` runs Werkzeug with `debug=True`.

## Git / GitHub

- Use [Conventional Commits](https://www.conventionalcommits.org/) format: prefix with `feat:`, `fix:`, `refactor:`, `chore:`, etc.
