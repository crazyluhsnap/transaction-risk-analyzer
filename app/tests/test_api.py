from fastapi.testclient import TestClient

from app.main import app

client=TestClient(app)

def test_root_endpoint():
    response=client.get("/")

    assert response.status_code==200

    assert response.json()=={
        "message":"Transaction Risk Analyzer API is running"
    }


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy"
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


def test_get_alerts():

    response = client.get("/alerts")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    assert len(data) > 0

    for alert in data:
        assert alert["risk_level"] == "HIGH"
        assert "transaction_id" in alert
        assert "risk_score" in alert
        assert "reasons" in alert


def test_get_alerts_contains_high_risk_transactions():

    response = client.get("/alerts")

    assert response.status_code == 200

    data = response.json()

    transaction_ids = {
        alert["transaction_id"]
        for alert in data
    }

    assert "T007" in transaction_ids
    assert "T008" in transaction_ids
    assert "T009" in transaction_ids


def test_get_summary():

    response = client.get("/summary")

    assert response.status_code == 200

    data = response.json()

    assert data["total_transactions"] == 15

    assert data["high_risk"] == 3
    assert data["medium_risk"] == 5
    assert data["low_risk"] == 7



def test_summary_counts_match_total():

    response = client.get("/summary")

    assert response.status_code == 200

    data = response.json()

    risk_total = (
        data["high_risk"]
        + data["medium_risk"]
        + data["low_risk"]
    )

    assert risk_total == data["total_transactions"]


def test_filter_transactions_by_count():
    response=client.get("/transactions?country=IN")
    assert response.status_code==200
    data=response.json()
    assert len(data)>0
    for transaction in data:
        assert transaction["country"]=="IN"

def test_filter_transactions_by_sender():
    response=client.get("/transactions?sender=A012")
    assert response.status_code==200
    data=response.json()
    assert len(data)>0
    for transaction in data:
        assert transaction["sender"]=="A012"

def test_filter_transactions_by_min_amount():
    response=client.get("/transactions?min_amount=100000")
    assert response.status_code==200
    data=response.json()
    assert len(data)>0
    for transaction in data:
        assert transaction["amount"]>=100000

def test_filter_transactions_with_multiple_filters():
    response=client.get(
        "/transactions?country=IN&min_amount=100000"
    )
    assert response.status_code==200
    data=response.json()
    for transaction in data:
        assert transaction["country"]=="IN"
        assert transaction["amount"]>=100000


def test_openapi_documentation():
    response=client.get("/openapi.json")

    assert response.status_code==200

    data=response.json()

    assert data["info"]["title"]=="Transaction Risk Analyzer"
    assert data['info']["version"]=="1.0.0"

    assert "/transactions" in data["paths"]
    assert "/transactions/{transaction_id}" in data["paths"]
    assert "/alerts" in data["paths"]
    assert "/summary" in data["paths"]
    assert "/analyze/{transaction_id}" in data["paths"]


def test_transactions_pagination():
    response = client.get("/transactions?limit=5&offset=0")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 5

def test_transactions_offset():
    response = client.get("/transactions?limit=5&offset=5")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 5
    assert data[0]["transaction_id"] == "T006"


def test_transactions_sort_by_amount_desc():
    response = client.get("/transactions?sort_by=amount&order=desc")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 15

    amounts = [transaction["amount"] for transaction in data]

    assert amounts == sorted(amounts, reverse=True)


def test_transactions_sort_by_amount_asc():
    response = client.get("/transactions?sort_by=amount&order=asc")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 15

    amounts = [transaction["amount"] for transaction in data]

    assert amounts == sorted(amounts)


def test_transactions_invalid_limit():
    response = client.get("/transactions?limit=-5")

    assert response.status_code == 422


def test_transactions_invalid_offset():
    response = client.get("/transactions?offset=-10")

    assert response.status_code == 422

def test_transactions_invalid_order():
    response = client.get("/transactions?order=invalid")

    assert response.status_code == 422

def test_transactions_invalid_sort_column():
    response = client.get("/transactions?sort_by=invalid")

    assert response.status_code == 422


def test_get_nonexistent_transaction():
    response=client.get("/transactions/INVALID")
    assert response.status_code==404
    data=response.json()
    assert "detail" in data

def test_analyze_nonexistent_transaction():
    response=client.post("/analyze/INVALID")
    assert response.status_code==404
    data=response.json()
    assert "detail" in data


def test_filter_transactions_by_transaction_id():
    response = client.get("/transactions?transaction_id=T007")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["transaction_id"] == "T007"

def test_filter_transactions_by_invalid_transaction_id():
    response = client.get("/transactions?transaction_id=INVALID")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 0


def test_filter_transactions_by_transaction_id_case_insensitive():
    response = client.get("/transactions?transaction_id=t004")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["transaction_id"] == "T004"