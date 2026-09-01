import networkx as nx

def build_transaction_graph(df):

    graph=nx.DiGraph()

    for _,row in df.iterrows():

        graph.add_edge(
            row["sender"],
            row["receiver"],
            transaction_id=row["transaction_id"],
            amount=row["amount"],
            timestamp=row["timestamp"],
            country=row["country"]
        )

    return graph