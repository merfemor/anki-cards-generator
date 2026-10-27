#!/usr/bin/env bash

set -e

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Load .env if present, without overriding existing environment variables.
if [[ -f "$SCRIPT_DIR/.env" ]]; then
    set -a
    source "$SCRIPT_DIR/.env"
    set +a
fi

if [[ "${OPEN_BROWSER:-0}" == "1" ]]; then
    (sleep 2; open "http://127.0.0.1:5000") &
fi

exec uv run gunicorn 'app.main:prod_entry()'
