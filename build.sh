#!/usr/bin/env bash
set -euo pipefail

# Build front + package back. Lance ce script depuis la racine du repo.
ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "==> Build frontend (Vite)"
cd "$ROOT_DIR/frontend"
npm install
npm run build

echo "==> Build backend (Poetry)"
cd "$ROOT_DIR"
poetry build

echo "✅ Build terminé. Front dans frontend/dist, artefacts Python dans dist/."

poetry run python -m backend.app
