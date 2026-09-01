from .risk_config import(
    CYCLE_AMOUNT_THRESHOLD,
    CYCLE_RISK_SCORE,
    CYCLE_WINDOW_MINUTES
)

def analyze_cycle(cycle):
    risk_score=0
    reasons=[]
    if cycle["duration_minutes"]<=CYCLE_WINDOW_MINUTES:
        if cycle["total_amount"]>CYCLE_AMOUNT_THRESHOLD:
            risk_score+=CYCLE_RISK_SCORE
            reasons.append("Rapid circular transaction pattern")

    return{
        "risk_score":risk_score,
        "reasons":reasons
    }

def get_network_risk_for_transaction(transaction_id,cycles):
    risk_score=0
    reasons=[]

    for cycle in cycles:
        if transaction_id in cycle["transactions"]:
            risk_score+=CYCLE_RISK_SCORE
            reasons.append("Rapid circular transaction pattern")

    return{
        "risk_score":risk_score,
        "reasons":reasons
    }