import pandas as pd

from .graph_builder import build_transaction_graph
from .networkx_cycle_detector import find_graph_cycles
from .cycle_mapper import map_cycle_to_transaction
from .cycle_analyzer import analyze_cycle_transactions

def analyze_network(df):
    df=df.copy()
    df["timestamp"]=pd.to_datetime(df["timestamp"])

    graph=build_transaction_graph(df)
    graph_cycles=find_graph_cycles(graph)

    analyzed_cycles=[]

    for cycle in graph_cycles:

        transactions=map_cycle_to_transaction(df,cycle)

        cycle_result=analyze_cycle_transactions(transactions)

        analyzed_cycles.append(cycle_result)

    return analyzed_cycles