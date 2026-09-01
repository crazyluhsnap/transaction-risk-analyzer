from .analyzer import analyze_transaction
from .account_analyzer import analyze_account
from .networkx_network_analyzer import analyze_network
from .network_risk import get_network_risk_for_transaction
from .risk_aggregator import calculate_final_risk


def analyze_transaction_risk(df, transaction):

    transaction_result = analyze_transaction(transaction)

    account_result = analyze_account(
        df,
        transaction["sender"],
        transaction["timestamp"]
    )

    cycles = analyze_network(df)

    network_result = get_network_risk_for_transaction(
        transaction["transaction_id"],
        cycles
    )

    final_result = calculate_final_risk(
        transaction_result,
        account_result,
        network_result
    )

    return final_result