from fastapi import FastAPI, HTTPException, Query
import pandas as pd
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware

from app.networkx_network_analyzer import analyze_network
from app.analysis_service import analyze_transaction_risk
from app.models import(
    HealthResponse,
    RiskAnalysisResponse,
    TransactionResponse,
    SummaryResponse
)

app=FastAPI(
    title="Transaction Risk Analyzer",
    description="API for analyzing transaction risk",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return{
        "message":"Transaction Risk Analyzer API is running"
    }


@app.get("/health", response_model=HealthResponse)
def health():
    return{
        "status":"healthy"
    }


@app.get("/transactions", response_model=list[TransactionResponse])
def get_transactions(
    country: str | None=None,
    sender: str | None=None,
    min_amount: float | None=None,
    risk_level: str | None = Query(None, pattern="^(LOW|MEDIUM|HIGH)$"),
    limit: int | None=Query(None,ge=1),
    offset: int = Query(0,ge=0),
    sort_by: str | None=None,
    order: str = Query("asc",pattern="^(asc|desc)$"),
    transaction_id: str | None=None
):
    df=pd.read_csv("data/transactions.csv")
    df["timestamp"]=pd.to_datetime(df["timestamp"]).astype(str)
    analysis_df = df.copy()

    if transaction_id is not None:
        df=df[df["transaction_id"].str.upper()==transaction_id.upper()]
    if country is not None:
        df=df[df["country"]==country]

    if sender is not None:
        df=df[df["sender"]==sender]

    if min_amount is not None:
        df=df[df["amount"]>=min_amount]

    if risk_level is not None:
        risk_levels = []

        for _, row in df.iterrows():
            transaction = row.to_dict()

            result = analyze_transaction_risk(
                analysis_df,
                transaction
            )

            risk_levels.append(result["risk_level"])

        df["risk_level"] = risk_levels
        df = df[df["risk_level"] == risk_level]
        df = df.drop(columns=["risk_level"])

    if sort_by is not None:
        allowed_sort_columns=[
            "transaction_id",
            "timestamp",
            "sender",
            "receiver",
            "amount",
            "country"
        ]
        if sort_by not in allowed_sort_columns:
            raise HTTPException(
                status_code=422,
                detail="Invalid sort column"
            )
        ascending=order.lower()=="asc"
        df=df.sort_values(by=sort_by,ascending=ascending)



    if limit is not None:
        df=df.iloc[offset:offset+limit]
    else:
        df=df.iloc[offset:]


    return df.to_dict(orient="records")


@app.get("/transactions/{transaction_id}", response_model=TransactionResponse)
def get_transaction(transaction_id: str):

    df=pd.read_csv("data/transactions.csv")

    df["timestamp"]=pd.to_datetime(df["timestamp"]).astype(str)

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


@app.get("/summary", response_model=SummaryResponse)
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



@app.post("/analyze/{transaction_id}",
          response_model=RiskAnalysisResponse)
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