import pandas as pd

from app.account_analyzer import analyze_account


def test_account_with_normal_activity():

    df = pd.DataFrame([
        {
            "transaction_id": "T001",
            "sender": "A001",
            "receiver": "A002",
            "amount": 1000,
            "timestamp": "2026-08-01 10:00:00"
        },
        {
            "transaction_id": "T002",
            "sender": "A001",
            "receiver": "A003",
            "amount": 1500,
            "timestamp": "2026-08-01 11:00:00"
        }
    ])

    result = analyze_account(
        df,
        "A001",
        "2026-08-01 11:00:00"
    )

    assert result["transaction_count"] == 2
    assert result["risk_score"] == 0
    assert result["reasons"] == []


def test_account_with_high_velocity():

    df = pd.DataFrame([
        {
            "transaction_id": "T011",
            "sender": "A012",
            "receiver": "A013",
            "amount": 1000,
            "timestamp": "2026-08-01 14:00:00"
        },
        {
            "transaction_id": "T012",
            "sender": "A012",
            "receiver": "A014",
            "amount": 1000,
            "timestamp": "2026-08-01 14:10:00"
        },
        {
            "transaction_id": "T013",
            "sender": "A012",
            "receiver": "A015",
            "amount": 1000,
            "timestamp": "2026-08-01 14:20:00"
        }
    ])

    result = analyze_account(
        df,
        "A012",
        "2026-08-01 14:20:00"
    )

    assert result["transaction_count"] == 3
    assert result["risk_score"] == 30
    assert "High transaction velocity" in result["reasons"]