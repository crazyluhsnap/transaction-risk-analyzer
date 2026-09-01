from fastapi import FastAPI, HTTPException
import pandas as pd

from app.networkx_network_analyzer import analyze_network
from app.analysis_service import analyze_transaction_risk

app=FastAPI(
    title="Transaction Risk Analyzer",
    description="API for analyzing transaction risk",
    version="1.0.0"
)

@app.get("/")
def root():
    return{
        "message":"Transaction Risk Analyzer API is running"
    }


@app.get("/transactions")
def get_transactions():
    df=pd.read_csv("data/transactions.csv")
    df["timestamp"]=pd.to_datetime(df["timestamp"])
    return df.to_dict(orient="records")


@app.get("/transactions/{transaction_id}")
def get_transaction(transaction_id: str):

    df=pd.read_csv("data/transactions.csv")

    df["timestamp"]=pd.to_datetime(df["timestamp"])

    transaction=df[
        df["transaction_id"]==transaction_id
    ]
    if transaction.empty:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    return transaction.iloc[0].to_dict()


@app.get("/alerts")
def get_alerts():
    df=pd.read_csv("data/transactions.csv")
    df["timestamp"]=pd.to_datetime(df["timestamp"])

    alerts=[]

    for _,row in df.iterrows():
        transaction=row.to_dict()

        result=analyze_transaction_risk(
            df,
            transaction
        )
        if result["risk_level"]=="HIGH":
            alerts.append(result)

    return alerts


@app.get("/summary")
def get_summary():

    df=pd.read_csv("data/transactions.csv")
    df["timestamp"]=pd.to_datetime(df["timestamp"])

    risk_counts={
        "HIGH":0,
        "MEDIUM":0,
        "LOW":0
    }

    for _,row in df.iterrows():
        transaction=row.to_dict()

        result=analyze_transaction_risk(
            df,transaction
        )

        risk_counts[result["risk_level"]]+=1

    return{
        "total_transactions":len(df),
        "high_risk":risk_counts["HIGH"],
        "medium_risk":risk_counts["MEDIUM"],
        "low_risk":risk_counts["LOW"]
    }



@app.post("/analyze/{transaction_id}")
def analyze(transaction_id: str):

    df=pd.read_csv("data/transactions.csv")
    df["timestamp"]=pd.to_datetime(df["timestamp"])

    transaction=df[
        df["transaction_id"]==transaction_id
    ]

    if transaction.empty:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    transaction=transaction.iloc[0].to_dict()

    result=analyze_transaction_risk(
        df,
        transaction
    )

    return result