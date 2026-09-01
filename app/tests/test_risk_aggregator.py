from app.risk_aggregator import calculate_final_risk


def test_high_risk_is_calculated_correctly():

    transaction_result = {
        "transaction_id": "T007",
        "risk_score": 30,
        "risk_level": "MEDIUM",
        "reasons": ["Large transaction"]
    }

    account_result = {
        "account_id": "A006",
        "transaction_count": 1,
        "risk_score": 0,
        "reasons": []
    }

    network_result = {
        "risk_score": 40,
        "reasons": ["Rapid circular transaction pattern"]
    }

    result = calculate_final_risk(
        transaction_result,
        account_result,
        network_result
    )

    assert result["transaction_id"] == "T007"

    assert result["risk_score"] == 70

    assert result["risk_level"] == "HIGH"

    assert result["reasons"] == [
        "Large transaction",
        "Rapid circular transaction pattern"
    ]


def test_low_risk_is_calculated_correctly():

    transaction_result = {
        "transaction_id": "T001",
        "risk_score": 0,
        "risk_level": "LOW",
        "reasons": []
    }

    account_result = {
        "account_id": "A001",
        "transaction_count": 1,
        "risk_score": 0,
        "reasons": []
    }

    network_result = {
        "risk_score": 0,
        "reasons": []
    }

    result = calculate_final_risk(
        transaction_result,
        account_result,
        network_result
    )

    assert result["transaction_id"] == "T001"

    assert result["risk_score"] == 0

    assert result["risk_level"] == "LOW"

    assert result["reasons"] == []