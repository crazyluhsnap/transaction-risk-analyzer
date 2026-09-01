import pandas as pd

from app.networkx_network_analyzer import analyze_network


def test_network_analyzer_detects_cycle():

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

    result = analyze_network(df)

    assert len(result) == 1

    cycle = result[0]

    assert set(cycle["transactions"]) == {
        "T007",
        "T008",
        "T009"
    }

    assert set(cycle["accounts"]) == {
        "A006",
        "A008",
        "A009"
    }

    assert cycle["total_amount"] == 525000

    assert cycle["duration_minutes"] == 10.0