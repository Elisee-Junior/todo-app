# Todo App (Flask + Vite/Vue/Tailwind)

Application TODO avec backend Flask et frontend Vite/Vue 3 + Tailwind.

## Prérequis
- Docker + Docker Compose (recommandé)
- OU : Python 3.10+ ; Node 18+ & npm

## Démarrage avec Docker (recommandé)
- `docker compose up --build`
- Frontend : http://localhost:8080
- API : http://localhost:5000 (également proxifiée via le front sur `/api`)

## Démarrage en local (sans Docker)
- Backend : `pip install -r backend/requirements.txt` puis `python backend/app.py` (port 5000)
- Frontend : `cd frontend && npm install && npm run dev` (port 5173, proxy vers 5000 pour `/api`)

## Build front pour servir via Flask
- `cd frontend && npm run build`
- Lancer le backend : `python backend/app.py`
- Accès : http://localhost:5000 (assets dans `frontend/dist`)

## API (mémoire volatile)
- GET /api/todos
- POST /api/todos { title }
- PUT /api/todos/:id { title?, completed? }
- DELETE /api/todos/:id
- GET /api/health

