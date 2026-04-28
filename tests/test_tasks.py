"""Tests for the /api/tasks CRUD endpoints."""

import json

HEADERS = {"Content-Type": "application/json"}


# ---------- GET (empty) ----------
def test_get_tasks_empty(client):
    resp = client.get("/api/tasks")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["count"] == 0
    assert data["tasks"] == []


# ---------- POST ----------
def test_create_task(client):
    payload = {"title": "Learn Docker", "description": "Containers 101"}
    resp = client.post("/api/tasks", data=json.dumps(payload), headers=HEADERS)
    assert resp.status_code == 201
    task = resp.get_json()
    assert task["id"] == 1
    assert task["title"] == "Learn Docker"
    assert task["completed"] is False


def test_create_task_without_title(client):
    resp = client.post("/api/tasks", data=json.dumps({}), headers=HEADERS)
    assert resp.status_code == 400


def test_create_task_empty_title(client):
    resp = client.post(
        "/api/tasks", data=json.dumps({"title": "   "}), headers=HEADERS
    )
    assert resp.status_code == 400


# ---------- GET by id ----------
def test_get_single_task(client):
    client.post(
        "/api/tasks",
        data=json.dumps({"title": "Task 1"}),
        headers=HEADERS,
    )
    resp = client.get("/api/tasks/1")
    assert resp.status_code == 200
    assert resp.get_json()["title"] == "Task 1"


def test_get_task_not_found(client):
    resp = client.get("/api/tasks/999")
    assert resp.status_code == 404


# ---------- PUT ----------
def test_update_task(client):
    client.post(
        "/api/tasks",
        data=json.dumps({"title": "Old"}),
        headers=HEADERS,
    )
    resp = client.put(
        "/api/tasks/1",
        data=json.dumps({"title": "New", "completed": True}),
        headers=HEADERS,
    )
    assert resp.status_code == 200
    task = resp.get_json()
    assert task["title"] == "New"
    assert task["completed"] is True


def test_update_task_not_found(client):
    resp = client.put(
        "/api/tasks/999",
        data=json.dumps({"title": "X"}),
        headers=HEADERS,
    )
    assert resp.status_code == 404


# ---------- DELETE ----------
def test_delete_task(client):
    client.post(
        "/api/tasks",
        data=json.dumps({"title": "To delete"}),
        headers=HEADERS,
    )
    resp = client.delete("/api/tasks/1")
    assert resp.status_code == 200

    resp = client.get("/api/tasks")
    assert resp.get_json()["count"] == 0


def test_delete_task_not_found(client):
    resp = client.delete("/api/tasks/999")
    assert resp.status_code == 404
