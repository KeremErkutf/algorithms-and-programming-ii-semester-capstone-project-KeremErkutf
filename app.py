# app.py

import streamlit as st
import networkx as nx
import matplotlib as plt
from algorithm import Graph, topological_sort_kahn, topological_sort_dfs
from visualizer import draw_graph
import json # For loading/saving graph examples

def parse_graph_input(input_string):
    """
    Parses a string of edges (e.g., "A,B\nC,D") into a Graph object.
    """
    g = Graph()
    if not input_string.strip():
        return g

    edges = input_string.strip().split('\n')
    for edge_str in edges:
        if ',' in edge_str:
            u, v = edge_str.split(',')
            g.add_edge(u.strip(), v.strip())
    return g

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
        "It's part of the Algorithms and Programming II course at Fırat University."
    )
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Assoc. Prof. Ferhat UÇAR**")
    st.sidebar.markdown("April 2025 - June 2025")

    # --- Graph Input Section ---
    st.header("Define Your Graph")
    st.markdown("Enter directed edges as `Source,Target` (e.g., `A,B`). Use a new line for each edge.")

    default_graph_input = "A,B\nA,C\nB,D\nC,D\nE,F"
    
    graph_input = st.text_area("Graph Edges:", value=default_graph_input, height=150, 
                               help="Each line represents a directed edge (e.g., A,B means A -> B)")

    # --- Algorithm Selection ---
    st.header("Select Algorithm and Visualize")
    algo_choice = st.selectbox("Choose Topological Sort Algorithm:",
                               ["Kahn's Algorithm (BFS-based)", "DFS-based Algorithm"])
    
    if st.button("Run Topological Sort"):
        st.session_state.graph = parse_graph_input(graph_input)
        
        if not st.session_state.graph.get_vertices():
            st.warning("Please enter some edges to define your graph.")
            del st.session_state.graph # Clear graph from session state
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
        # This prevents the layout from changing with each step
        dummy_graph = nx.DiGraph()
        dummy_graph.add_nodes_from(st.session_state.graph.get_vertices())
        for u, neighbors in st.session_state.graph.get_adj_list().items():
            for v in neighbors:
                dummy_graph.add_edge(u, v)
        st.session_state.initial_pos = nx.spring_layout(dummy_graph, k=0.8, iterations=50) # Use a fixed layout

    if 'sorted_steps' in st.session_state:
        st.subheader("Algorithm Visualization")
        
        # Display sorted order if not cycled
        if st.session_state.cycle_detected:
            st.error("Cycle detected! Topological sort is not possible for this graph.")
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
                st.pyplot(fig) # Display the matplotlib figure
                #plt.close(fig) # Close the figure to prevent memory leaks

        else:
            st.info("No steps to visualize for this graph (e.g., empty graph).")
    
    st.markdown("---")
    st.subheader("Complexity Analysis (To be documented in README.md)")
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