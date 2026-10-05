import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app  # noqa: E402
from app.models import db  # noqa: E402


@pytest.fixture()
def app():
    app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:", "SECRET_KEY": "test-secret-key-for-unit-tests-only-0123456789"})
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def make_user(client):
    """Register a user and return the Authorization header for them."""

    def _make(username="alice", email=None, password="correct-horse"):
        email = email or f"{username}@example.com"
        client.post("/api/auth/register", json={"username": username, "email": email, "password": password})
        token = client.post("/api/auth/login", json={"username": username, "password": password}).get_json()["token"]
        return {"Authorization": f"Bearer {token}"}

    return _make
