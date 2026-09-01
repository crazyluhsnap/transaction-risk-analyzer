from app.network_risk import get_network_risk_for_transaction


def test_transaction_inside_cycle_gets_network_risk():

    cycles = [
        {
            "transactions": ["T007", "T008", "T009"],
            "accounts": ["A006", "A008", "A009"],
            "total_amount": 525000,
            "duration_minutes": 10.0
        }
    ]

    result = get_network_risk_for_transaction(
        "T007",
        cycles
    )

    assert result["risk_score"] == 40

    assert result["reasons"] == [
        "Rapid circular transaction pattern"
    ]


def test_transaction_outside_cycle_has_no_network_risk():

    cycles = [
        {
            "transactions": ["T007", "T008", "T009"],
            "accounts": ["A006", "A008", "A009"],
            "total_amount": 525000,
            "duration_minutes": 10.0
        }
    ]

    result = get_network_risk_for_transaction(
        "T001",
        cycles
    )

    assert result["risk_score"] == 0

    assert result["reasons"] == []