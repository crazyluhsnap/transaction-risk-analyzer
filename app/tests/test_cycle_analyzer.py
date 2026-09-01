import pandas as pd

from app.graph_builder import build_transaction_graph
from app.networkx_cycle_detector import find_graph_cycles
from app.cycle_mapper import map_cycle_to_transaction
from app.cycle_analyzer import analyze_cycle_transactions


def test_cycle_is_analyzed_correctly():

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

    graph = build_transaction_graph(df)

    cycles = find_graph_cycles(graph)

    cycle = cycles[0]

    transactions = map_cycle_to_transaction(
        df,
        cycle
    )

    result = analyze_cycle_transactions(
        transactions
    )

    assert set(result["transactions"]) == {
        "T007",
        "T008",
        "T009"
    }

    assert set(result["accounts"]) == {
        "A006",
        "A008",
        "A009"
    }

    assert result["total_amount"] == 525000

    assert result["duration_minutes"] == 10.0