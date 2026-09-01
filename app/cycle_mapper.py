def map_cycle_to_transaction(df,cycle):
    transactions=[]

    for i in range(len(cycle)):
        sender=cycle[i]
        receiver=cycle[(i+1)%len(cycle)]

        matches=df[
            (df["sender"]==sender)
            &
            (df["receiver"]==receiver)
        ]
        for _,row in matches.iterrows():
            transactions.append({
                "transaction_id":row["transaction_id"],
                "sender":row["sender"],
                "receiver":row["receiver"],
                "amount":row["amount"],
                "timestamp":row["timestamp"]
            })
    return transactions