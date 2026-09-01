from fastapi.testclient import TestClient

from app.main import app

client=TestClient(app)

def test_root_endpoint():
    response=client.get("/")

    assert response.status_code==200

    assert response.json()=={
        "message":"Transaction Risk Analyzer API is running"
    }


def test_analyze_high_risk_transaction():
    response=client.post("/analyze/T007")
    assert response.status_code==200

    data=response.json()

    assert data["transaction_id"]=="T007"
    assert data["risk_score"]==70
    assert data["risk_level"]=="HIGH"

    assert "Large transaction" in data["reasons"]
    assert "Rapid circular transaction pattern" in data["reasons"]


def test_analyze_unknown_transaction():
    response=client.post("/analyze/DOES_NOT_EXIST")

    assert response.status_code==404

    assert response.json()["detail"]=="Transaction not found"

    