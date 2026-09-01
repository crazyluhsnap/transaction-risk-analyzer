import pandas as pd
from .risk_config import(
    HIGH_VELOCITY_THRESHOLD,
    HIGH_VELOCITY_SCORE
)

def analyze_velocity(df, account_id,transaction_time):
    account_transactions=df[df["sender"]==account_id].copy()

    account_transactions["timestamp"]=pd.to_datetime(
        account_transactions["timestamp"]
    )

    transaction_time=pd.to_datetime(transaction_time)

    window_start=transaction_time-pd.Timedelta(minutes=30)

    transactions_in_window=account_transactions[
        (account_transactions["timestamp"]>=window_start)
        &
        (account_transactions["timestamp"]<=transaction_time)
    ]
    transaction_count=len(transactions_in_window)

    risk_score=0
    reasons=[]

    if transaction_count>=HIGH_VELOCITY_THRESHOLD:
        risk_score=HIGH_VELOCITY_SCORE
        reasons.append("High transaction velocity")

    return{
        "account_id":account_id,
        "risk_score":risk_score,
        "reasons":reasons,
        "transactions_in_window":transaction_count
    }