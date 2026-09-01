import pandas as pd
from .velocity_analyzer import analyze_velocity
from .risk_config import(
    HIGH_FREQUENCY_THRESHOLD,
    HIGH_FREQUENCY_SCORE
)

def analyze_account(df, account_id, transaction_time):

    df = df.copy()

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    transaction_time = pd.to_datetime(transaction_time)

    account_transactions = df[
        (df["sender"] == account_id)
        &
        (df["timestamp"] <= transaction_time)
    ]

    transaction_count = len(account_transactions)

    risk_score = 0
    reasons = []

    if transaction_count >= HIGH_FREQUENCY_THRESHOLD:
        risk_score += HIGH_FREQUENCY_SCORE
        reasons.append("High transaction frequency")

    velocity_result = analyze_velocity(
        df,
        account_id,
        transaction_time
    )

    risk_score += velocity_result["risk_score"]
    reasons.extend(velocity_result["reasons"])

    return {
        "account_id": account_id,
        "transaction_count": transaction_count,
        "risk_score": risk_score,
        "reasons": reasons
    }
