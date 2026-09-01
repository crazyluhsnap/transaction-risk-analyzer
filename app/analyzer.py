from .risk_config import(
    LARGE_TRANSACTION_SCORE,
    LARGE_TRANSACTION_THRESHOLD,
    HIGH_RISK_COUNTRIES,
    HIGH_RISK_COUNTRY_SCORE,
    CRITICAL_THRESHOLD,
    HIGH_THRESHOLD,
    MEDIUM_THRESHOLD
)

def analyze_transaction(transaction):
    risk_score=0
    reasons=[]
    amount=transaction["amount"]
    country=transaction["country"]

    if country in HIGH_RISK_COUNTRIES:
        risk_score+=HIGH_RISK_COUNTRY_SCORE
        reasons.append("High risk country")

    if amount>LARGE_TRANSACTION_THRESHOLD:
        risk_score+=LARGE_TRANSACTION_SCORE
        reasons.append("Large transaction")

    if risk_score>=CRITICAL_THRESHOLD:
        risk_level="CRITICAL"
    elif risk_score>=HIGH_THRESHOLD:
        risk_level="HIGH"
    elif risk_score>=MEDIUM_THRESHOLD:
        risk_level="MEDIUM"
    else:
        risk_level="LOW"

    return{
        "transaction_id":transaction["transaction_id"],
        "risk_score":risk_score,
        "risk_level":risk_level,
        "reasons":reasons
    }