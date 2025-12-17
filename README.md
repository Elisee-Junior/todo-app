# Todo App (Flask + Vite/Vue/Tailwind)

Application TODO avec backend Flask et frontend Vite/Vue 3 + Tailwind.

## Prérequis
- Python 3.10+
- Node 18+ et npm
- Poetry (`pip install poetry`) pour le backend

## Installation
- Backend : `poetry install`
- Frontend : `cd frontend && npm install`

## Développement
- Lancer l’API : `poetry run python -m backend.app` (port 5000)
- Lancer le front : `cd frontend && npm run dev` (port 5173, proxy vers l’API)

## Build front pour servir via Flask
- `cd frontend && npm run build`
- Relancer l’API : `poetry run python -m backend.app`
- Accès : http://localhost:5000 (assets dans `frontend/dist`)

## Build backend (wheel/sdist)
- `poetry build` (sorties dans `dist/`)

## API (mémoire volatile)
- GET /api/todos
- POST /api/todos { title }
- PUT /api/todos/:id { title?, completed? }
- DELETE /api/todos/:id

