from .risk_config import(
    CRITICAL_THRESHOLD,
    HIGH_THRESHOLD,
    MEDIUM_THRESHOLD
)

def calculate_final_risk(transaction_result,account_result,network_result):
    final_score=(
        transaction_result["risk_score"]+
        account_result["risk_score"]+
        network_result["risk_score"]
    )
    reasons=(
        transaction_result["reasons"]+
        account_result["reasons"]+
        network_result["reasons"]
    )
    if final_score>=CRITICAL_THRESHOLD:
        risk_level="CRITICAL"
    elif final_score>=HIGH_THRESHOLD:
        risk_level="HIGH"
    elif final_score>=MEDIUM_THRESHOLD:
        risk_level="MEDIUM"
    else:
        risk_level="LOW"

    return{
        "transaction_id":transaction_result["transaction_id"],
        "risk_score":final_score,
        "risk_level":risk_level,
        "reasons":reasons
    }