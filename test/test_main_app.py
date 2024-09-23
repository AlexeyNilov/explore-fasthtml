import pytest
from starlette.testclient import TestClient

from main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_title(client):
    r = client.get("/")
    assert "<title>Main app</title>" in r.text
