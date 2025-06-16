# app.py

import streamlit as st
from algorithm import Graph, topological_sort_kahn, topological_sort_dfs
from visualizer import draw_graph
import networkx as nx 
import matplotlib.pyplot as plt 
import json 
import time # Animasyon için time modülüne yine ihtiyacımız var, burayı aktif ettik!

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
        stripped_edge_str = edge_str.strip()
        if ',' in stripped_edge_str:
            u, v = stripped_edge_str.split(',')
            g.add_edge(u.strip(), v.strip()) 
        elif stripped_edge_str != "":
            # Handle single nodes without explicit edges: add node to graph's vertices set
            if stripped_edge_str not in g.vertices:
                g.vertices.add(stripped_edge_str)
                g.num_vertices = len(g.vertices)
            # Ensure it has an indegree entry even if 0
            if stripped_edge_str not in g.indegree:
                g.indegree[stripped_edge_str] = 0

    return g

def parse_json_graph(json_data):
    """
    Parses graph data from a JSON object.
    Expects 'edges' as a list of [source, target] lists.
    Optional: 'nodes' as a list of node names.
    """
    g = Graph()
    
    if "nodes" in json_data and isinstance(json_data["nodes"], list):
        for node in json_data["nodes"]:
            if node not in g.vertices:
                g.vertices.add(node)
                g.num_vertices = len(g.vertices)
            if node not in g.indegree:
                g.indegree[node] = 0 # Initialize indegree for all nodes

    if "edges" in json_data and isinstance(json_data["edges"], list):
        for edge in json_data["edges"]:
            if isinstance(edge, list) and len(edge) == 2:
                u, v = str(edge[0]).strip(), str(edge[1]).strip()
                g.add_edge(u, v)
            else:
                st.warning(f"Invalid edge format in JSON: {edge}. Skipping.")
    else:
        st.warning("JSON file does not contain a valid 'edges' list.")
        
    return g

# --- Example Graphs (for text area default) ---
EXAMPLE_GRAPHS = {
    "Simple DAG": "A,B\nA,C\nB,D\nC,D",
    "Complex DAG": "A,B\nA,C\nB,D\nC,E\nD,F\nE,F\nG,H\nG,I\nH,J\nI,J",
    "Graph with Cycle": "A,B\nB,C\nC,A", 
    "Disconnected Graph": "X,Y\nP,Q\nR,S",
    "Isolated Nodes (A,B,C)": "A\nB\nC", 
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
    st.markdown("You can either load an example graph, upload a JSON file, or define your own manually.")

    # JSON File Uploader
    uploaded_file = st.file_uploader("Upload a JSON Graph File", type="json", help="Upload a .json file containing graph edges (e.g., {'edges': [['A','B'], ['B','C']]}) and optionally 'nodes'.")

    example_choice = st.selectbox("Or Load Example Graph:", list(EXAMPLE_GRAPHS.keys()), key="example_selector")
    
    if "graph_input_text_area" not in st.session_state:
        st.session_state.graph_input_text_area = EXAMPLE_GRAPHS[example_choice]
    
    if st.session_state.example_selector != st.session_state.get('last_example_choice_for_text_area', None):
        st.session_state.graph_input_text_area = EXAMPLE_GRAPHS[example_choice]
        st.session_state.last_example_choice_for_text_area = st.session_state.example_selector

    graph_input = st.text_area("Or enter your own graph edges (e.g., `A,B\nC,D`):", 
                               value=st.session_state.graph_input_text_area, height=150, 
                               help="Each line represents a directed edge (e.g., A,B means A -> B). For isolated nodes, enter the node name on its own line (e.g., 'A').",
                               key="graph_input_text_area_key")
    
    # --- Algorithm Selection ---
    st.header("Select Algorithm and Visualize")
    algo_choice = st.selectbox("Choose Topological Sort Algorithm:",
                               ["Kahn's Algorithm (BFS-based)", "DFS-based Algorithm"], key="algo_selector")
    
    # Initialize session state variables for animation and step control
    if "current_step_index" not in st.session_state:
        st.session_state.current_step_index = 0
    if "is_playing" not in st.session_state:
        st.session_state.is_playing = False


    if st.button("Run Topological Sort", key="run_algo_button"):
        st.session_state.current_step_index = 0 # Reset to first step on run
        st.session_state.is_playing = False # Stop any ongoing animation
        
        graph_to_process = None
        if uploaded_file is not None:
            try:
                # Read JSON data from uploaded file
                json_data = json.load(uploaded_file)
                graph_to_process = parse_json_graph(json_data)
                st.success("Graph loaded successfully from JSON file!")
            except json.JSONDecodeError:
                st.error("Invalid JSON file. Please upload a valid JSON.")
                graph_to_process = None
            except Exception as e:
                st.error(f"An error occurred while processing the JSON file: {e}")
                graph_to_process = None
        elif graph_input.strip() != "":
            graph_to_process = parse_graph_input(graph_input)
            st.info("Graph loaded from text input.")
        else:
            st.warning("Please enter graph edges or upload a JSON file to run the algorithm.")
            # Clear previous state if no valid input
            if 'sorted_steps' in st.session_state: del st.session_state.sorted_steps
            if 'initial_pos' in st.session_state: del st.session_state.initial_pos
            st.rerun() # Rerun to clear UI

        if graph_to_process is None or (not graph_to_process.get_vertices() and graph_to_process.num_vertices == 0):
            st.error("No valid graph could be constructed from the input. Please check your data.")
            if 'sorted_steps' in st.session_state: del st.session_state.sorted_steps
            if 'initial_pos' in st.session_state: del st.session_state.initial_pos
            st.stop() # Stop execution if no valid graph
        
        st.session_state.graph = graph_to_process

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
        dummy_graph.add_nodes_from(st.session_state.graph.get_vertices()) 
        for u, neighbors in st.session_state.graph.get_adj_list().items():
            for v in neighbors:
                dummy_graph.add_edge(u, v)
        if len(dummy_graph.nodes()) > 0: 
            st.session_state.initial_pos = nx.spring_layout(dummy_graph, k=0.8, iterations=50) 
        else: # Handle empty graph case for layout
            st.session_state.initial_pos = {} 
        st.rerun() 


    # --- Algorithm Visualization Section ---
    if 'sorted_steps' in st.session_state and len(st.session_state.sorted_steps) > 0:
        st.subheader("Algorithm Visualization")
        
        # Display sorted order or cycle detection message
        if st.session_state.cycle_detected:
            st.error("Cycle detected in the graph! Topological sort is not possible.")
            st.write("Vertices processed before cycle detection (if any): ", st.session_state.final_sorted_order)
        else:
            st.success(f"Final Topological Sort Order: {st.session_state.final_sorted_order}")

        num_steps = len(st.session_state.sorted_steps)
        
        # --- Sidebar Controls ---
        st.sidebar.markdown("---")
        st.sidebar.subheader("Animation Controls")
        
        # Animation Play/Stop and Speed
        anim_col1, anim_col2 = st.sidebar.columns(2)
        with anim_col1:
            if st.button("Play Animation", key="play_button", 
                         disabled=st.session_state.is_playing or st.session_state.current_step_index >= num_steps - 1):
                st.session_state.is_playing = True
                # st.session_state.current_step_index = 0 # Start from the beginning when playing, if desired
                st.rerun()

        with anim_col2:
            if st.button("Stop Animation", key="stop_button", disabled=not st.session_state.is_playing):
                st.session_state.is_playing = False
                st.rerun()
        
        animation_speed = st.sidebar.slider("Delay (seconds)", 0.1, 2.0, 0.5, 0.1, key="animation_speed_slider",
                                            help="Delay between steps during animation.")

        st.sidebar.markdown("---")
        st.sidebar.subheader("Step Navigation")
        
        # Sidebar Previous/Next Buttons
        sidebar_col1, sidebar_col2 = st.sidebar.columns(2)
        with sidebar_col1:
            if st.button("Previous Step", key="prev_step_button", 
                         disabled=(st.session_state.current_step_index == 0 or st.session_state.is_playing)):
                st.session_state.current_step_index = max(0, st.session_state.current_step_index - 1)
                st.rerun()
        
        with sidebar_col2:
            if st.button("Next Step", key="next_step_button", 
                         disabled=(st.session_state.current_step_index >= num_steps - 1 or st.session_state.is_playing)):
                st.session_state.current_step_index = min(num_steps - 1, st.session_state.current_step_index + 1)
                st.rerun()
        
        # Sidebar Slider
        # Slider disabled when playing animation
        st.sidebar.slider("Current Step Index", 0, num_steps - 1, st.session_state.current_step_index, 
                           key="step_slider_sidebar", help="Drag to view different stages of the algorithm.", 
                           disabled=st.session_state.is_playing)
        
        # If slider is manually moved (and not playing), update the current_step_index
        if not st.session_state.is_playing and st.session_state.step_slider_sidebar != st.session_state.current_step_index:
            st.session_state.current_step_index = st.session_state.step_slider_sidebar
            st.rerun()


        # --- Main Content Area for Visualization and Details using columns ---
        # Splitting the main content area into two columns for graph and step details
        vis_col, info_col = st.columns([1, 1]) # Ratio 1:1 for visualization vs. info

        with vis_col:
            st.markdown("### Graph Visualization")
            current_step_data = st.session_state.sorted_steps[st.session_state.current_step_index]
            fig, pos = draw_graph(st.session_state.graph, current_step_data, st.session_state.initial_pos)
            if fig:
                st.pyplot(fig) 
                plt.close(fig) # Close the figure to prevent memory leaks

        with info_col:
            st.markdown("### Step Details")
            st.markdown(f"**Step:** {st.session_state.current_step_index + 1} / {num_steps}")
            st.info(f"**Description:** {current_step_data['message']}")

            if st.session_state.algo_choice == "Kahn's Algorithm (BFS-based)":
                st.write(f"**Current Queue:** {current_step_data.get('queue', [])}")
                st.write(f"**Current Indegrees:** {current_step_data.get('indegree', {})}")
            elif st.session_state.algo_choice == "DFS-based Algorithm":
                st.write(f"**Visited Status (0: Unvisited, 1: Visiting, 2: Visited):** {current_step_data.get('visited_status', {})}")
                st.write(f"**Recursion Stack:** {current_step_data.get('recursion_stack', {})}")
            
            st.write(f"**Sorted List So Far:** {current_step_data.get('sorted_list', [])}")
            
        # Animation Loop Logic (Conditional Rerun)
        # This logic must be outside the `with vis_col:` or `with info_col:` blocks
        # to ensure it can trigger a full rerun
        if st.session_state.is_playing:
            # We animate up to num_steps-1. When it hits num_steps-1, it displays that step,
            # then next rerun current_step_index becomes num_steps (out of bounds), stopping animation.
            if st.session_state.current_step_index < num_steps -1 : 
                time.sleep(animation_speed)
                st.session_state.current_step_index += 1
                st.rerun() 
            else: # Animation finished (reached last step)
                st.session_state.is_playing = False
                st.info("Animation finished!")
                # st.session_state.current_step_index = num_steps - 1 # This line might cause infinite loop on some edge cases
                st.rerun() 

    else:
        st.info("Run an algorithm to see the visualization steps here.")
    
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