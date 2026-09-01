import pandas as pd

from app.networkx_network_analyzer import analyze_network
from app.analysis_service import analyze_transaction_risk

df=pd.read_csv("data/transactions.csv")
df["timestamp"]=pd.to_datetime(df["timestamp"])
cycles=analyze_network(df)


for _,row in df.iterrows():
    transaction=row.to_dict()

    result=analyze_transaction_risk(
        df,
        transaction,
        cycles
    )

    print(result)
