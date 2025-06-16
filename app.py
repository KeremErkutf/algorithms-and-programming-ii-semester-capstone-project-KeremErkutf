# app.py

import streamlit as st
from algorithm import Graph, topological_sort_kahn, topological_sort_dfs
from visualizer import draw_graph
import networkx as nx 
import matplotlib.pyplot as plt 

def parse_graph_input(input_string):
    """
    Parses a string of edges (e.g., "A,B\nC,D") into a Graph object.
    Cleans node names by stripping whitespace.
    """
    g = Graph()
    if not input_string.strip():
        return g

    edges = input_string.strip().split('\n')
    for edge_str in edges:
        if ',' in edge_str:
            u, v = edge_str.split(',')
            g.add_edge(u.strip(), v.strip()) # Strip whitespace from node names
    return g

# --- Example Graphs (New addition) ---
EXAMPLE_GRAPHS = {
    "Simple DAG": "A,B\nA,C\nB,D\nC,D",
    "Complex DAG": "A,B\nA,C\nB,D\nC,E\nD,F\nE,F\nG,H\nG,I\nH,J\nI,J",
    "Graph with Cycle": "A,B\nB,C\nC,A", # This should detect a cycle
    "Disconnected Graph": "X,Y\nP,Q\nR,S",
    "Single Node Graph": "A", # No edges, just a node
    "Empty Graph": ""
}

def main():
    """
    Main function to run the Streamlit application.
    """
    st.set_page_config(page_title="Topological Sort Visualizer", layout="wide")
    st.title("Topological Sort Algorithm Visualizer")
    st.write("Welcome to the Semester Capstone Project for Algorithms and Programming II!")
    st.markdown("This application allows you to visualize and understand the **Topological Sort algorithm**.")

    st.sidebar.header("About")
    st.sidebar.info(
        "This project implements and visualizes the Topological Sort algorithm. "
        "It's part of the Algorithms and Programming II course at Fırat University, Software Engineering Department."
    )
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Assoc. Prof. Ferhat UÇAR**")
    st.sidebar.markdown("April 2025 - June 2025")

    # --- Graph Input Section ---
    st.header("Define Your Graph")
    st.markdown("You can either load an example graph or define your own.")

    # Load example graph
    example_choice = st.selectbox("Load Example Graph:", list(EXAMPLE_GRAPHS.keys()))
    
    # Custom graph input
    graph_input = st.text_area("Or enter your own graph edges (e.g., `A,B\nC,D`):", 
                               value=EXAMPLE_GRAPHS[example_choice], height=150, 
                               help="Each line represents a directed edge (e.g., A,B means A -> B). Isolated nodes can be added like 'A' (if no edges leave/enter them).")

    # --- Algorithm Selection ---
    st.header("Select Algorithm and Visualize")
    algo_choice = st.selectbox("Choose Topological Sort Algorithm:",
                               ["Kahn's Algorithm (BFS-based)", "DFS-based Algorithm"])
    
    if st.button("Run Topological Sort"):
        st.session_state.graph = parse_graph_input(graph_input)
        
        if not st.session_state.graph.get_vertices() and graph_input.strip() != "":
            # This handles cases like "A" where it's a single node but not an edge
            # We need to ensure single nodes are added to vertices if not part of an edge
            # For simplicity, if no edges, the parse_graph_input creates an empty graph.
            # We can refine this later if pure single nodes are a must.
            st.warning("Please enter valid edges to define your graph or select a proper example.")
            del st.session_state.graph # Clear graph from session state
            if 'sorted_steps' in st.session_state:
                del st.session_state.sorted_steps
            if 'initial_pos' in st.session_state:
                del st.session_state.initial_pos
            return
        elif not st.session_state.graph.get_vertices() and graph_input.strip() == "":
            st.warning("Graph is empty. Please enter some edges or select an example.")
            if 'sorted_steps' in st.session_state:
                del st.session_state.sorted_steps
            if 'initial_pos' in st.session_state:
                del st.session_state.initial_pos
            return


        if algo_choice == "Kahn's Algorithm (BFS-based)":
            sorted_order, cycle_detected, steps = topological_sort_kahn(st.session_state.graph)
        else: # DFS-based Algorithm
            sorted_order, cycle_detected, steps = topological_sort_dfs(st.session_state.graph)
        
        st.session_state.sorted_steps = steps
        st.session_state.final_sorted_order = sorted_order
        st.session_state.cycle_detected = cycle_detected
        st.session_state.algo_choice = algo_choice
        
        # Generate initial fixed positions for consistency during steps
        dummy_graph = nx.DiGraph()
        # Ensure all vertices from the actual graph are included for layout
        dummy_graph.add_nodes_from(st.session_state.graph.get_vertices())
        for u, neighbors in st.session_state.graph.get_adj_list().items():
            for v in neighbors:
                dummy_graph.add_edge(u, v)
        st.session_state.initial_pos = nx.spring_layout(dummy_graph, k=0.8, iterations=50) 

    if 'sorted_steps' in st.session_state:
        st.subheader("Algorithm Visualization")
        
        # Display sorted order if not cycled
        if st.session_state.cycle_detected:
            st.error("Cycle detected in the graph! Topological sort is not possible.")
            st.write("Vertices processed before cycle detection (if any): ", st.session_state.final_sorted_order)
        else:
            st.success(f"Final Topological Sort Order: {st.session_state.final_sorted_order}")

        num_steps = len(st.session_state.sorted_steps)
        if num_steps > 0:
            step_index = st.slider("Select Step", 0, num_steps - 1, 0, help="Drag to view different stages of the algorithm.")
            current_step_data = st.session_state.sorted_steps[step_index]
            
            st.markdown(f"---")
            st.markdown(f"### Current Step: {step_index + 1} / {num_steps}")
            st.info(f"**Description:** {current_step_data['message']}")

            # Display additional algorithm-specific info
            if st.session_state.algo_choice == "Kahn's Algorithm (BFS-based)":
                st.write(f"**Current Queue:** {current_step_data.get('queue', [])}")
                st.write(f"**Current Indegrees:** {current_step_data.get('indegree', {})}")
            elif st.session_state.algo_choice == "DFS-based Algorithm":
                st.write(f"**Visited Status (0: Unvisited, 1: Visiting, 2: Visited):** {current_step_data.get('visited_status', {})}")
                st.write(f"**Recursion Stack:** {current_step_data.get('recursion_stack', {})}")
            
            st.write(f"**Sorted List So Far:** {current_step_data.get('sorted_list', [])}")


            # Draw the graph for the current step
            fig, pos = draw_graph(st.session_state.graph, current_step_data, st.session_state.initial_pos)
            if fig:
                st.pyplot(fig) 
                # plt.close(fig) # Removed this line in previous fix
        else:
            st.info("No steps to visualize for this graph (e.g., empty graph).")
    
    st.markdown("---")
    st.subheader("Complexity Analysis (Also in README.md)")
    st.write(
        """
        - **Time Complexity (Kahn's Algorithm):** $O(V + E)$ where V is the number of vertices and E is the number of edges.
          Each vertex and each edge is processed once.
        - **Space Complexity (Kahn's Algorithm):** $O(V + E)$ for adjacency list, indegree array, and queue.

        - **Time Complexity (DFS-based Algorithm):** $O(V + E)$ where V is the number of vertices and E is the number of edges.
          Each vertex and each edge is visited once.
        - **Space Complexity (DFS-based Algorithm):** $O(V + E)$ for adjacency list, visited array, and recursion stack (call stack).
        """
    )
    st.markdown("---")


if __name__ == "__main__":
    main()