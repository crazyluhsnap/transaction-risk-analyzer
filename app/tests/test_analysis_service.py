import pandas as pd

from app.analysis_service import analyze_transaction_risk


def test_analysis_service_detects_high_risk_transaction():

    df = pd.DataFrame([
        {
            "transaction_id": "T007",
            "sender": "A006",
            "receiver": "A008",
            "amount": 180000,
            "timestamp": "2026-08-01 14:15:00",
            "country": "IN"
        },
        {
            "transaction_id": "T008",
            "sender": "A008",
            "receiver": "A009",
            "amount": 175000,
            "timestamp": "2026-08-01 14:20:00",
            "country": "IN"
        },
        {
            "transaction_id": "T009",
            "sender": "A009",
            "receiver": "A006",
            "amount": 170000,
            "timestamp": "2026-08-01 14:25:00",
            "country": "IN"
        }
    ])

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    transaction = df.iloc[0].to_dict()

    result = analyze_transaction_risk(
        df,
        transaction
    )

    assert result["transaction_id"] == "T007"

    assert result["risk_score"] == 70

    assert result["risk_level"] == "HIGH"

    assert "Large transaction" in result["reasons"]

    assert "Rapid circular transaction pattern" in result["reasons"]