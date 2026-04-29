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