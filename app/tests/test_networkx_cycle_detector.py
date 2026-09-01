import pandas as pd

from app.graph_builder import build_transaction_graph
from app.networkx_cycle_detector import find_graph_cycles


def test_cycle_is_detected():

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

    assert len(cycles) == 1

    cycle = cycles[0]

    assert set(cycle) == {"A006", "A008", "A009"}