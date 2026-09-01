import networkx as nx

def find_graph_cycles(graph):
    cycles=list(nx.simple_cycles(graph))

    return cycles