import pandas as pd
def find_cycles(df):
    cycles=[]
    seen_cycles=set()
    df["timestamp"]=pd.to_datetime(df["timestamp"])

    for _,t1 in df.iterrows():
        for _,t2 in df.iterrows():
            for _,t3 in df.iterrows():

                if(
                    t1["receiver"]==t2["sender"]
                    and
                    t2["receiver"]==t3["sender"]
                    and
                    t3["receiver"]==t1["sender"]
                ):
                    start_time=min(
                        t1["timestamp"],
                        t2["timestamp"],
                        t3["timestamp"]
                    )
                    end_time=max(
                        t1["timestamp"],
                        t2["timestamp"],
                        t3["timestamp"]
                    )
                    time_difference=end_time-start_time

                    if time_difference<=pd.Timedelta(minutes=30):
                        total_amount=(
                            t1["amount"]+
                            t2["amount"]+
                            t3["amount"]
                        )
                        duration_minutes=time_difference.total_seconds()/60
                        accounts=[
                            t1["sender"],
                            t1["receiver"],
                            t2["receiver"]
                        ]

                        cycle=tuple(sorted([
                            t1["transaction_id"],
                            t2["transaction_id"],
                            t3["transaction_id"]
                        ]))

                        if cycle not in seen_cycles:
                            cycle_info={
                                "transactions":list(cycle),
                                "accounts":accounts,
                                "total_amount":total_amount,
                                "duration_minutes":duration_minutes
                            }
                            cycles.append(cycle_info)
                            seen_cycles.add(cycle)
                    

    return cycles