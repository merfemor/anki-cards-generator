#!/usr/bin/env bash

echo "Starting http server on http://localhost:8000/"
SCRIPT_DIR=$(dirname "$0")
python -m http.server 8000 -d $SCRIPT_DIR/src