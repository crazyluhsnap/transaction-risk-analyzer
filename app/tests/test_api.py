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


def test_get_transactions():

    response = client.get("/transactions")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    assert len(data) > 0

    assert "transaction_id" in data[0]
    assert "sender" in data[0]
    assert "receiver" in data[0]
    assert "amount" in data[0]
    assert "timestamp" in data[0]


def test_get_transaction():

    response = client.get("/transactions/T007")

    assert response.status_code == 200

    data = response.json()

    assert data["transaction_id"] == "T007"
    assert data["sender"] == "A006"
    assert data["receiver"] == "A008"
    assert data["amount"] == 180000


def test_get_transaction_not_found():

    response = client.get("/transactions/T999")

    assert response.status_code == 404

    data = response.json()

    assert data["detail"] == "Transaction not found"