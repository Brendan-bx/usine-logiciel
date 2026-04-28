"""Main application module with all routes and business logic."""

import logging
import os
import sys

from flask import Flask, jsonify, request
from prometheus_flask_exporter import PrometheusMetrics

# ---------------------------------------------------------------------------
# Application factory
# ---------------------------------------------------------------------------
app = Flask(__name__)

# ---------------------------------------------------------------------------
# Logging configuration
# ---------------------------------------------------------------------------
_log_level = os.environ.get("LOG_LEVEL", "INFO")
_log_handlers = [logging.StreamHandler(sys.stdout)]

_log_dir = os.environ.get("LOG_DIR", "")
if _log_dir:
    os.makedirs(_log_dir, exist_ok=True)
    _log_handlers.append(logging.FileHandler(os.path.join(_log_dir, "app.log")))

logging.basicConfig(
    level=getattr(logging, _log_level, logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=_log_handlers,
)
logger = logging.getLogger("taskmanager")

# ---------------------------------------------------------------------------
# Prometheus metrics
# ---------------------------------------------------------------------------
metrics = PrometheusMetrics(app)
metrics.info("app_info", "Task Manager API", version="1.0.0")

# ---------------------------------------------------------------------------
# In-memory storage
# ---------------------------------------------------------------------------
tasks_db: list[dict] = []
_task_id_counter: int = 0


def _next_id() -> int:
    global _task_id_counter
    _task_id_counter += 1
    return _task_id_counter


def _find_task(task_id: int) -> dict | None:
    return next((t for t in tasks_db if t["id"] == task_id), None)


def reset_state() -> None:
    """Reset application state — used by tests."""
    global _task_id_counter
    tasks_db.clear()
    _task_id_counter = 0


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.route("/health", methods=["GET"])
@metrics.do_not_track()
def health_check():
    """Health-check endpoint."""
    return jsonify({"status": "healthy", "service": "task-manager"}), 200


@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    """Return every task."""
    logger.info("Fetching all tasks")
    return jsonify({"tasks": tasks_db, "count": len(tasks_db)}), 200


@app.route("/api/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    """Return a single task by ID."""
    task = _find_task(task_id)
    if not task:
        logger.warning("Task %s not found", task_id)
        return jsonify({"error": "Task not found"}), 404
    return jsonify(task), 200


@app.route("/api/tasks", methods=["POST"])
def create_task():
    """Create a new task (title required)."""
    data = request.get_json(silent=True)
    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    title = data["title"]
    if not isinstance(title, str) or len(title.strip()) == 0:
        return jsonify({"error": "Title must be a non-empty string"}), 400

    task = {
        "id": _next_id(),
        "title": title.strip(),
        "description": data.get("description", ""),
        "completed": False,
    }
    tasks_db.append(task)
    logger.info("Task created: %s — %s", task["id"], task["title"])
    return jsonify(task), 201


@app.route("/api/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    """Update an existing task."""
    task = _find_task(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "No data provided"}), 400

    if "title" in data:
        task["title"] = data["title"]
    if "description" in data:
        task["description"] = data["description"]
    if "completed" in data:
        task["completed"] = bool(data["completed"])

    logger.info("Task updated: %s", task_id)
    return jsonify(task), 200


@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    """Delete a task."""
    global tasks_db
    task = _find_task(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    tasks_db = [t for t in tasks_db if t["id"] != task_id]
    logger.info("Task deleted: %s", task_id)
    return jsonify({"message": f"Task {task_id} deleted"}), 200


# ---------------------------------------------------------------------------
# Entry-point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
