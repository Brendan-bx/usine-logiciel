import json
from unittest.mock import patch

HEADERS = {"Content-Type": "application/json"}


# ===== MOCK LOGGER =====

@patch("app.main.logger")
def test_create_task_calls_logger(mock_logger, client):
    """Créer une tâche doit écrire un log."""
    client.post(
        "/api/tasks",
        data=json.dumps({"title": "Test"}),
        headers=HEADERS,
    )
    mock_logger.info.assert_called_once()


@patch("app.main.logger")
def test_delete_task_calls_logger(mock_logger, client):
    """Supprimer une tâche doit écrire un log."""
    client.post(
        "/api/tasks",
        data=json.dumps({"title": "A supprimer"}),
        headers=HEADERS,
    )
    mock_logger.reset_mock()

    client.delete("/api/tasks/1")
    mock_logger.info.assert_called_once()


@patch("app.main.logger")
def test_get_unknown_task_logs_warning(mock_logger, client):
    """Chercher une tâche inexistante doit écrire un warning."""
    client.get("/api/tasks/999")
    mock_logger.warning.assert_called_once()

# ===== MOCK _find_task =====


@patch("app.main._find_task")
def test_get_task_uses_find(mock_find, client):
    """GET /api/tasks/1 doit appeler _find_task(1)."""
    mock_find.return_value = {
        "id": 1, "title": "Fake", "description": "", "completed": False
    }
    resp = client.get("/api/tasks/1")
    assert resp.status_code == 200
    assert resp.get_json()["title"] == "Fake"
    mock_find.assert_called_once_with(1)


@patch("app.main._find_task")
def test_get_task_not_found_returns_404(mock_find, client):
    """_find_task retourne None → 404."""
    mock_find.return_value = None
    resp = client.get("/api/tasks/999")
    assert resp.status_code == 404


@patch("app.main._find_task")
def test_delete_not_found_returns_404(mock_find, client):
    """_find_task retourne None lors d'un DELETE → 404."""
    mock_find.return_value = None
    resp = client.delete("/api/tasks/42")
    assert resp.status_code == 404

# ===== MOCK _next_id =====


@patch("app.main._next_id")
def test_create_task_uses_next_id(mock_next_id, client):
    """La création doit utiliser _next_id pour générer l'ID."""
    mock_next_id.return_value = 99

    resp = client.post(
        "/api/tasks",
        data=json.dumps({"title": "ID mocké"}),
        headers=HEADERS,
    )
    assert resp.status_code == 201
    assert resp.get_json()["id"] == 99
    mock_next_id.assert_called_once()

# ===== MOCK STORAGE =====


@patch("app.main.tasks_db", new_callable=lambda: list)
def test_get_tasks_with_fake_data(mock_db, client):
    """Injecter des fausses données et vérifier la réponse."""
    mock_db.extend([
        {"id": 1, "title": "Fausse tâche A", "description": "", "completed": False},
        {"id": 2, "title": "Fausse tâche B", "description": "", "completed": True},
    ])

    resp = client.get("/api/tasks")
    assert resp.status_code == 200
    assert resp.get_json()["count"] == 2


@patch("app.main.tasks_db", new_callable=lambda: list)
def test_get_single_fake_task(mock_db, client):
    """Récupérer une tâche depuis un stockage mocké."""
    mock_db.append(
        {"id": 5, "title": "Mocké", "description": "test", "completed": True}
    )

    resp = client.get("/api/tasks/5")
    assert resp.status_code == 200
    assert resp.get_json()["title"] == "Mocké"
    assert resp.get_json()["completed"] is True
