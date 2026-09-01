import pandas as pd
df=pd.read_csv("data/transactions.csv")
print(df)
print()
print(df.info())
print()
print(df.head())#first 5 entries
print(len(df))#no of transactions
print(df['amount'].sum())