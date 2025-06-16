# visualizer.py

import networkx as nx
import matplotlib.pyplot as plt
import streamlit as st

def draw_graph(graph_obj, current_step_data=None, pos=None):
    """
    Draws the graph with nodes and edges, highlighting elements based on the current algorithm step.

    Args:
        graph_obj (Graph): The Graph object containing nodes and edges.
        current_step_data (dict, optional): Data for the current step from the algorithm's 'steps' list.
                                            Used for highlighting. Defaults to None.
        pos (dict, optional): A dictionary of node positions (e.g., {node: [x,y]}).
                              If None, a spring layout is generated. Useful for consistent layouts.
    """
    G = nx.DiGraph()
    
    # Add nodes to NetworkX graph
    all_vertices = graph_obj.get_vertices()
    if not all_vertices: # Handle empty graph
        st.write("No nodes in the graph to visualize.")
        return None, None

    G.add_nodes_from(all_vertices)

    # Add edges to NetworkX graph
    for u, neighbors in graph_obj.get_adj_list().items():
        for v in neighbors:
            G.add_edge(u, v)

    # Define node colors and labels
    node_colors = []
    node_labels = {}
    
    # Default node styling
    default_node_color = 'skyblue'
    current_node_color = 'red' # Highlight for currently processed node
    queue_node_color = 'lightgreen' # Highlight for nodes in queue (Kahn's)
    visited_visiting_color = 'orange' # For DFS: visiting state
    visited_finished_color = 'grey' # For DFS: visited/finished state
    
    # Default edge styling
    default_edge_color = 'gray'
    highlight_edge_color = 'red' # Highlight for active edge being explored
    edge_colors = [default_edge_color] * len(G.edges())
    
    # indegree labels for Kahn's
    indegree_labels = {} 
    if current_step_data and "indegree" in current_step_data:
        indegree_data = current_step_data["indegree"]
        for v in all_vertices:
            indegree_labels[v] = f"{v} (in:{indegree_data.get(v, 0)})"
    else:
        for v in all_vertices:
            indegree_labels[v] = str(v)


    # Apply styling based on current_step_data
    if current_step_data:
        current_node = current_step_data.get("current_node")
        queue_nodes = current_step_data.get("queue", []) # For Kahn's
        visited_status = current_step_data.get("visited_status", {}) # For DFS
        recursion_stack = current_step_data.get("recursion_stack", {}) # For DFS
        
        for node in all_vertices:
            if node == current_node:
                node_colors.append(current_node_color)
            elif node in queue_nodes: # Kahn's specific
                node_colors.append(queue_node_color)
            elif visited_status.get(node) == 1: # DFS: visiting
                node_colors.append(visited_visiting_color)
            elif visited_status.get(node) == 2: # DFS: visited/finished
                node_colors.append(visited_finished_color)
            elif recursion_stack.get(node): # DFS: in recursion stack (potential cycle)
                node_colors.append('purple') # Indicate it's in recursion stack
            else:
                node_colors.append(default_node_color)
        
        # Highlight current edge being processed (e.g., for DFS exploration)
        if "source_node" in current_step_data and "target_node" in current_step_data:
            highlighted_edge = (current_step_data["source_node"], current_step_data["target_node"])
            for i, edge in enumerate(G.edges()):
                if edge == highlighted_edge:
                    edge_colors[i] = highlight_edge_color

    else: # No step data, all default color
        node_colors = [default_node_color] * len(all_vertices)

    # Generate node positions if not provided for consistency
    if pos is None:
        pos = nx.spring_layout(G, k=0.8, iterations=50) # k and iterations can be tuned for better layouts
    
    fig, ax = plt.subplots(figsize=(10, 7)) # Create a matplotlib figure and axes
    
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=2000, ax=ax)
    
    # Draw edges
    nx.draw_networkx_edges(G, pos, edge_color=edge_colors, arrowsize=20, ax=ax)
    
    # Draw labels (use indegree labels if available, else node name)
    nx.draw_networkx_labels(G, pos, labels=indegree_labels if indegree_labels else {node: node for node in G.nodes()}, font_size=10, font_weight='bold', ax=ax)
    
    # If a cycle is detected, highlight it
    if current_step_data and current_step_data.get("type") == "cycle_detection" or current_step_data.get("cycle_detected"):
        ax.set_title("CYCLE DETECTED!", color='red', fontsize=16)
        st.error("Cycle detected! Topological sort not possible for this graph.")
    elif current_step_data and current_step_data.get("type") == "final_result" and not current_step_data.get("cycle_detected"):
        ax.set_title("Topological Sort Completed", color='green', fontsize=16)
    else:
        ax.set_title("Topological Sort Visualization", fontsize=16)
    
    ax.set_axis_off() # Hide axes
    
    return fig, pos # Return the figure and positions for consistent layout