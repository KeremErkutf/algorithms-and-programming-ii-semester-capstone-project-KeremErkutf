import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def draw_graph(graph, step_data, initial_pos):
    """
    Draws the graph using NetworkX and Matplotlib, highlighting elements based on step_data.
    Args:
        graph (Graph): The Graph object containing nodes and edges.
        step_data (dict): Dictionary containing current step's information (e.g., 'current_node', 'highlighted_nodes', 'message').
        initial_pos (dict): Pre-calculated initial positions for nodes to maintain consistency.
    Returns:
        tuple: A tuple containing the matplotlib figure and the node positions.
    """
    G = nx.DiGraph()

    # Add all nodes first, so disconnected nodes also appear
    G.add_nodes_from(graph.get_vertices())

    for u, neighbors in graph.get_adj_list().items():
        for v in neighbors:
            G.add_edge(u, v)

    # Use initial_pos if available, otherwise calculate a new layout
    if initial_pos:
        pos = initial_pos
    else:
        # Optimized spring_layout parameters to reduce node overlap
        # Increased iterations to allow the layout algorithm more time to settle.
        # Adjusted 'k' (optimal distance) to potentially spread nodes out better.
        pos = nx.spring_layout(G, k=0.6, iterations=100) 
    
    # --- Figure size adjustment ---
    # Adjusted figsize to make the plot even shorter vertically.
    # (width, height) in inches. Trying (6, 3.5) for a more compact vertical space.
    fig, ax = plt.subplots(figsize=(6, 3.5)) # Dikey eksende daha kısa bir boyut (6x3.5 inç)

    # Node coloring based on step_data
    node_colors = []
    # Default color for all nodes
    default_node_color = '#ADD8E6' # Light Blue

    # Highlighted nodes (e.g., in queue, visiting, visited)
    highlighted_nodes = step_data.get('highlighted_nodes', [])
    # Current node being processed
    current_node = step_data.get('current_node', None)
    # DFS visited statuses
    visited_status = step_data.get('visited_status', {}) # 0: Unvisited, 1: Visiting, 2: Visited

    for node in G.nodes():
        if node == current_node:
            node_colors.append('#FF6347') # Tomato Red for current node
        elif node in highlighted_nodes:
            node_colors.append('#FFA07A') # Light Salmon for highlighted (e.g., in queue)
        elif node in visited_status:
            status = visited_status.get(node, 0)
            if status == 1: # Visiting (DFS specific)
                node_colors.append('#FFD700') # Gold
            elif status == 2: # Visited (DFS specific)
                node_colors.append('#90EE90') # Light Green
            else:
                node_colors.append(default_node_color)
        else:
            node_colors.append(default_node_color)

    # Draw nodes
    # Reduced node_size further for a more compact visualization.
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=1000, ax=ax) # node_size 1000 olarak değiştirildi

    # Draw edges
    # Standard edges
    nx.draw_networkx_edges(G, pos, ax=ax, edgelist=G.edges(), arrowstyle='->', arrowsize=20, edge_color='gray', width=1.5)

    # Highlight current edge if available
    current_edge = step_data.get('current_edge', None)
    if current_edge:
        nx.draw_networkx_edges(G, pos, ax=ax, edgelist=[current_edge], arrowstyle='->', arrowsize=25, edge_color='red', width=2.5)

    # Draw labels
    # Reduced font_size for labels to fit within smaller nodes.
    nx.draw_networkx_labels(G, pos, font_size=7, font_weight='bold', ax=ax) # font_size 7 olarak değiştirildi

    ax.set_title("Graph Visualization", size=15)
    ax.set_axis_off() # Hide axes
    
    return fig, pos