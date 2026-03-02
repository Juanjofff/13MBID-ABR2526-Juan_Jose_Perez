#!/usr/bin/env bash
# Script de arranque para Render: usar "python -m uvicorn" para que encuentre uvicorn
set -e
exec python -m uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8000}"
