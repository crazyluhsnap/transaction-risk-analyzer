import pandas as pd

from app.velocity_analyzer import analyze_velocity


def test_low_velocity():

    df = pd.DataFrame([
        {
            "transaction_id": "T011",
            "sender": "A012",
            "receiver": "A013",
            "amount": 1000,
            "timestamp": "2026-08-01 14:00:00"
        }
    ])

    result = analyze_velocity(
        df,
        "A012",
        "2026-08-01 14:00:00"
    )

    assert result["risk_score"] == 0
    assert result["transactions_in_window"] == 1
    assert result["reasons"] == []


def test_high_velocity():

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

    result = analyze_velocity(
        df,
        "A012",
        "2026-08-01 14:20:00"
    )

    assert result["risk_score"] == 30
    assert result["transactions_in_window"] == 3
    assert "High transaction velocity" in result["reasons"]