import pytest

from backend.app import app, _todos


@pytest.fixture(autouse=True)
def clear_store():
    _todos.clear()
    yield
    _todos.clear()


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_health(client):
    res = client.get("/api/test_ci")
    assert res.status_code == 200
    data = res.get_json()
    assert data["status"] == "ok"
    assert data["env"] == "dev"


def test_create_and_list(client):
    create = client.post("/api/todos", json={"title": "Task"})
    assert create.status_code == 201
    created = create.get_json()
    assert created["title"] == "Task"
    assert created["completed"] is False
    assert created["id"]

    listing = client.get("/api/todos")
    assert listing.status_code == 200
    todos = listing.get_json()
    assert len(todos) == 1
    assert todos[0]["title"] == "Task"

