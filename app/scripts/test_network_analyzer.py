import pandas as pd

from network_analyzer import find_cycles

df=pd.read_csv("data/transactions.csv")
df["timestamp"]=pd.to_datetime(df["timestamp"])

new_transactions = pd.DataFrame([
    {
        "transaction_id": "T016",
        "sender": "A020",
        "receiver": "A021",
        "amount": 10000,
        "country": "IN",
        "timestamp": "2026-08-01 10:00"
    },
    {
        "transaction_id": "T017",
        "sender": "A021",
        "receiver": "A022",
        "amount": 9000,
        "country": "IN",
        "timestamp": "2026-08-01 11:00"
    },
    {
        "transaction_id": "T018",
        "sender": "A022",
        "receiver": "A020",
        "amount": 8000,
        "country": "IN",
        "timestamp": "2026-08-01 12:00"
    }
])

df = pd.concat([df, new_transactions], ignore_index=True)

cycles=find_cycles(df)
for cycle in cycles:
    print(cycle)
