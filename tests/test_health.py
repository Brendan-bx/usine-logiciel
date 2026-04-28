"""Tests for the health-check endpoint."""


def test_health_returns_200(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "healthy"


def test_health_contains_service_name(client):
    resp = client.get("/health")
    assert resp.get_json()["service"] == "task-manager"
