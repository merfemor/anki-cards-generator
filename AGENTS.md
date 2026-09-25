# AI Coding Agent Instructions — anki-cards-generator

Python 3.11 project that generates Anki flashcards for learning German/English words, with translations (DeepL), sentence examples (LLM: Ollama or OpenAI), and TTS audio (macOS `say`).

## Tech stack

- Flask (async) web app with a web UI
- `uv` for dependency management
- Ruff (lint + format) + mypy for type checking
- pytest for tests
- Pre-commit hooks configured

## Run

```bash
uv run -m app          # start web UI at :5000
uv run pytest           # run tests
pre-commit run -a       # lint, format, type-check
```

## Code conventions

- Line length: 120 (enforced by Ruff).
- Use type hints on all function signatures.
- Source code lives under `src/app/`, tests under `tests/`.
- Async I/O (LLM calls, translations, TTS) uses `async`/`await`.
- The `main.py` module owns the Flask app and route handlers; business logic is delegated to separate modules (`*_data_extract`, `*_anki_generate`, etc.).
