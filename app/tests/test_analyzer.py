from app.analyzer import analyze_transaction


def test_large_transaction():
    transaction = {
        "transaction_id": "T005",
        "sender": "A004",
        "receiver": "A006",
        "amount": 150000,
        "country": "IN"
    }

    result = analyze_transaction(transaction)

    assert result["risk_score"] == 30
    assert result["risk_level"] == "MEDIUM"
    assert "Large transaction" in result["reasons"]


def test_normal_transaction():
    transaction = {
        "transaction_id": "T001",
        "sender": "A001",
        "receiver": "A002",
        "amount": 1500,
        "country": "IN"
    }

    result = analyze_transaction(transaction)

    assert result["risk_score"] == 0
    assert result["risk_level"] == "LOW"
    assert result["reasons"] == []


def test_high_risk_country():
    transaction = {
        "transaction_id": "T002",
        "sender": "A007",
        "receiver": "A001",
        "amount": 1500,
        "country": "XX"
    }

    result = analyze_transaction(transaction)

    assert result["risk_score"] == 30
    assert result["risk_level"] == "MEDIUM"
    assert "High risk country" in result["reasons"]


def test_high_risk_transaction():
    transaction = {
        "transaction_id": "T007",
        "sender": "A009",
        "receiver": "A008",
        "amount": 150000,
        "country": "YY"
    }

    result = analyze_transaction(transaction)

    assert result["risk_score"] == 60
    assert result["risk_level"] == "HIGH"
    assert "High risk country" in result["reasons"]
    assert "Large transaction" in result["reasons"]