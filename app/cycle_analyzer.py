def analyze_cycle_transactions(transactions):

    transaction_ids=[
        transaction["transaction_id"]
        for transaction in transactions
    ]

    accounts=[]

    for transaction in transactions:
        if transaction["sender"] not in accounts:
            accounts.append(transaction["sender"])

    total_amount=sum(
        transaction["amount"]
        for transaction in transactions
    )

    timestamps=[
        transaction["timestamp"]
        for transaction in transactions
    ]

    start_time=min(timestamps)
    end_time=max(timestamps)

    duration=end_time-start_time

    duration_minutes=duration.total_seconds()/60

    return{
        "transactions":transaction_ids,
        "accounts":accounts,
        "total_amount":total_amount,
        "duration_minutes":duration_minutes
    }