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