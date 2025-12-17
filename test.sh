#!/usr/bin/env bash
set -euo pipefail

# Lance la suite de tests backend avec pytest.
ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT_DIR"

# Force Poetry to use a cache inside the repo to avoid permission issues.
export POETRY_CACHE_DIR="$ROOT_DIR/.cache/pypoetry"
mkdir -p "$POETRY_CACHE_DIR"

echo "==> Installation des dépendances (inclut dev)"
poetry install --with dev

echo "==> Exécution des tests"
poetry run pytest

echo "✅ Tests terminés."
