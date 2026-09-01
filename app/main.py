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