import os

os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from backend.app import app, db, Task


def setup_module():
    with app.app_context():
        db.drop_all()
        db.create_all()


def teardown_module():
    with app.app_context():
        db.session.remove()
        db.drop_all()


def test_health():
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {
        "status": "healthy"
    }


def test_create_task():
    client = app.test_client()

    response = client.post(
        "/tasks",
        json={
            "title": "Test CI Task",
            "status": "pending"
        }
    )

    assert response.status_code == 201

    data = response.get_json()
    assert data["title"] == "Test CI Task"
    assert data["status"] == "pending"


def test_get_tasks():
    client = app.test_client()

    response = client.get("/tasks")

    assert response.status_code == 200

    data = response.get_json()

    assert isinstance(data, list)
    assert len(data) >= 1


def test_create_task_without_title():
    client = app.test_client()

    response = client.post(
        "/tasks",
        json={
            "status": "pending"
        }
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "Title is required"


def test_update_task():
    client = app.test_client()

    response = client.get("/tasks")
    tasks = response.get_json()

    task_id = tasks[0]["id"]

    response = client.put(
        f"/tasks/{task_id}",
        json={
            "status": "completed"
        }
    )

    assert response.status_code == 200
    assert response.get_json()["status"] == "completed"


def test_delete_task():
    client = app.test_client()

    response = client.get("/tasks")
    tasks = response.get_json()

    task_id = tasks[0]["id"]

    response = client.delete(f"/tasks/{task_id}")

    assert response.status_code == 200
    assert response.get_json()["message"] == "Task deleted successfully"
