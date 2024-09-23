import pytest
from starlette.testclient import TestClient

from sample.refresh import app


@pytest.fixture
def client():
    return TestClient(app)


def test_title(client):
    r = client.get("/")
    assert "<title>Self refresh app</title>" in r.text
