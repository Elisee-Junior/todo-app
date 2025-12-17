#!/usr/bin/env bash
set -euo pipefail

# Lance la suite de tests backend avec pytest.
ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT_DIR"

echo "==> Installation des dépendances (inclut dev)"
poetry install --with dev

echo "==> Exécution des tests"
poetry run pytest

echo "✅ Tests terminés."

