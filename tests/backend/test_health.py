from fastapi.testclient import TestClient

from backend.main import app


def test_root_and_health_endpoints():
    client = TestClient(app)
    assert client.get("/").status_code == 200
    health = client.get("/health")
    assert health.status_code == 200
    assert health.json()["status"] == "online"