from fastapi.testclient import TestClient
from app.main import app

def test_health():
    with TestClient(app) as client:
        resp = client.get("/health")
        assert resp.status_code == 200
        assert resp.json() == {"status": "ok"}


def test_list_foodtrucks():
    with TestClient(app) as client:
        resp = client.get("/api/foodtrucks")
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)


def test_nearby_requires_params():
    with TestClient(app) as client:
        resp = client.get("/api/foodtrucks/nearby")
        assert resp.status_code == 422
