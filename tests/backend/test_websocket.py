from fastapi.testclient import TestClient

from backend.main import app


def test_websocket_accepts_analysis_start_message():
    client = TestClient(app)
    with client.websocket_connect("/ws/audio") as websocket:
        websocket.send_json({"type": "start_analysis"})
        response = websocket.receive_json()
        assert response["status"] == "analysis_started"