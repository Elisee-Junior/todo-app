import os
import uuid
from flask import Flask, jsonify, request, send_from_directory, abort
from flask_cors import CORS

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DIST_DIR = os.path.join(BASE_DIR, "frontend", "dist")
MISSING_FRONTEND_MSG = (
    "Frontend non construit. Depuis `frontend/`: npm install && npm run build."
)

app = Flask(__name__, static_folder=DIST_DIR, static_url_path="")
CORS(app)

# Very small in-memory store. Replace with a database for production use.
_todos = []


def _find_todo(todo_id: str):
    return next((todo for todo in _todos if todo["id"] == todo_id), None)


@app.get("/api/todos")
def list_todos():
    return jsonify(_todos)


@app.get("/api/health")
def health():
    return jsonify({"status": "ok", "env": "dev"})


@app.post("/api/todos")
def create_todo():
    data = request.get_json(silent=True) or {}
    title = (data.get("title") or "").strip()

    if not title:
        return jsonify({"error": "title is required"}), 400

    todo = {
        "id": str(uuid.uuid4()),
        "title": title,
        "completed": bool(data.get("completed", False)),
    }
    _todos.append(todo)
    return jsonify(todo), 201


@app.put("/api/todos/<todo_id>")
def update_todo(todo_id: str):
    todo = _find_todo(todo_id)
    if not todo:
        return jsonify({"error": "not found"}), 404

    data = request.get_json(silent=True) or {}

    if "title" in data:
        new_title = (data.get("title") or "").strip()
        if not new_title:
            return jsonify({"error": "title cannot be empty"}), 400
        todo["title"] = new_title

    if "completed" in data:
        todo["completed"] = bool(data.get("completed"))

    return jsonify(todo)


@app.delete("/api/todos/<todo_id>")
def delete_todo(todo_id: str):
    todo = _find_todo(todo_id)
    if not todo:
        return jsonify({"error": "not found"}), 404

    _todos.remove(todo)
    return jsonify({"status": "deleted", "id": todo_id})


@app.get("/")
def serve_index():
    index_path = os.path.join(app.static_folder, "index.html")
    if not os.path.isfile(index_path):
        return MISSING_FRONTEND_MSG, 500

    return send_from_directory(app.static_folder, "index.html")


@app.get("/<path:path>")
def serve_static(path: str):
    if path.startswith("api/"):
        abort(404)

    file_path = os.path.join(app.static_folder, path)
    if os.path.isfile(file_path):
        return send_from_directory(app.static_folder, path)

    index_path = os.path.join(app.static_folder, "index.html")
    if os.path.isfile(index_path):
        return send_from_directory(app.static_folder, "index.html")

    return MISSING_FRONTEND_MSG, 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

