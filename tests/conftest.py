"""Shared fixtures for pytest."""

import pytest
from app.main import app as flask_app, reset_state


@pytest.fixture()
def client():
    """Provide a Flask test client."""
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as c:
        yield c


@pytest.fixture(autouse=True)
def _clean_state():
    """Ensure every test starts with an empty database."""
    reset_state()
    yield
    reset_state()
