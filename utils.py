# utils.py

import networkx as nx

def generate_graph_layout(graph_obj, k=0.8, iterations=50):
    """
    Generates node positions for a graph using NetworkX's spring layout.

    Args:
        graph_obj (Graph): The Graph object.
        k (float): Optimal distance between nodes (adjust for tighter/looser layouts).
        iterations (int): Number of iterations for the layout algorithm to run.

    Returns:
        dict: A dictionary of node positions (e.g., {node: [x,y]}).
    """
    dummy_graph = nx.DiGraph()
    dummy_graph.add_nodes_from(graph_obj.get_vertices())
    for u, neighbors in graph_obj.get_adj_list().items():
        for v in neighbors:
            dummy_graph.add_edge(u, v)
    
    if len(dummy_graph.nodes()) > 0:
        return nx.spring_layout(dummy_graph, k=k, iterations=iterations)
    else:
        return {} # Return empty dict for empty graph
