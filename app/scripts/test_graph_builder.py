import pandas as pd

from graph_builder import build_transaction_graph

df=pd.read_csv("data/transactions.csv")

df["timestamp"]=pd.to_datetime(df["timestamp"])

graph=build_transaction_graph(df)

print("Nodes: ",list(graph.nodes))
print("Edges: ",list(graph.edges))
print("Number of nodes: ",graph.number_of_nodes())
print("Number of edges: ",graph.number_of_edges())