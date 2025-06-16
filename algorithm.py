# algorithm.py

from collections import defaultdict, deque

class Graph:
    """
    Represents a directed graph using an adjacency list.
    """
    def __init__(self, num_vertices=0):
        """
        Initializes a graph with a given number of vertices.
        Adjacency list stores neighbors, indegree stores incoming edge count for each vertex.
        """
        self.num_vertices = num_vertices
        self.adj = defaultdict(list)  # Adjacency list: vertex -> list of neighbors
        self.indegree = defaultdict(int) # Indegree for Kahn's algorithm
        self.vertices = set() # To keep track of all vertices added

    def add_edge(self, u, v):
        """
        Adds a directed edge from vertex u to vertex v.
        Updates adjacency list and indegree.
        """
        if u not in self.vertices:
            self.vertices.add(u)
            self.num_vertices += 1
        if v not in self.vertices:
            self.vertices.add(v)
            self.num_vertices += 1

        self.adj[u].append(v)
        self.indegree[v] += 1

    def get_vertices(self):
        """Returns a sorted list of all unique vertices in the graph."""
        return sorted(list(self.vertices))

    def get_adj_list(self):
        """Returns the adjacency list."""
        return self.adj

    def get_indegree(self):
        """Returns the indegree mapping for all vertices."""
        return self.indegree


def topological_sort_kahn(graph):
    """
    Performs topological sorting using Kahn's algorithm (BFS-based).
    Returns a tuple: (sorted_list, cycle_detected, steps).
    steps: A list of dictionaries, each describing a step in the algorithm for visualization.
    """
    in_degree = graph.get_indegree().copy()
    q = deque()
    sorted_list = []
    num_processed_nodes = 0
    steps = []

    # Initialize queue with all vertices having an indegree of 0
    # Ensure all vertices are considered, even isolated ones
    for v in graph.get_vertices():
        if in_degree[v] == 0:
            q.append(v)
            steps.append({
                "type": "initialization",
                "message": f"Vertex {v} has an indegree of 0. Adding to queue.",
                "current_node": v,
                "queue": list(q),
                "sorted_list": list(sorted_list),
                "indegree": dict(in_degree)
            })

    # Process nodes in the queue
    while q:
        u = q.popleft()
        sorted_list.append(u)
        num_processed_nodes += 1
        steps.append({
            "type": "process_node",
            "message": f"Processing vertex {u}. Added to sorted list. Queue: {list(q)}.",
            "current_node": u,
            "queue": list(q),
            "sorted_list": list(sorted_list),
            "indegree": dict(in_degree)
        })

        # Decrease indegree of adjacent vertices
        for v in graph.get_adj_list()[u]:
            in_degree[v] -= 1
            steps.append({
                "type": "update_indegree",
                "message": f"Decreased indegree of {v} to {in_degree[v]} due to processing {u}.",
                "current_node": v,
                "source_node": u,
                "queue": list(q),
                "sorted_list": list(sorted_list),
                "indegree": dict(in_degree)
            })
            if in_degree[v] == 0:
                q.append(v)
                steps.append({
                    "type": "add_to_queue",
                    "message": f"Indegree of {v} became 0. Adding {v} to queue.",
                    "current_node": v,
                    "queue": list(q),
                    "sorted_list": list(sorted_list),
                    "indegree": dict(in_degree)
                })

    cycle_detected = num_processed_nodes != graph.num_vertices
    if cycle_detected:
        steps.append({
            "type": "cycle_detection",
            "message": "Cycle detected! Not all vertices could be processed.",
            "current_node": None,
            "queue": list(q),
            "sorted_list": list(sorted_list),
            "indegree": dict(in_degree)
        })
    else:
        steps.append({
            "type": "finished",
            "message": "Topological sort completed successfully.",
            "current_node": None,
            "queue": list(q),
            "sorted_list": list(sorted_list),
            "indegree": dict(in_degree)
        })

    return sorted_list, cycle_detected, steps


def topological_sort_dfs(graph):
    """
    Performs topological sorting using DFS-based algorithm.
    Returns a tuple: (sorted_list, cycle_detected, steps).
    steps: A list of dictionaries, each describing a step in the algorithm for visualization.
    """
    visited = defaultdict(int)  # 0: unvisited, 1: visiting, 2: visited
    recursion_stack = defaultdict(bool) # To detect cycles during DFS
    sorted_list = []
    steps = []
    cycle_detected = False

    def dfs_util(u):
        nonlocal cycle_detected
        visited[u] = 1 # Mark as visiting
        recursion_stack[u] = True # Add to recursion stack
        steps.append({
            "type": "dfs_visit",
            "message": f"Visiting node {u}.",
            "current_node": u,
            "visited_status": dict(visited),
            "recursion_stack": dict(recursion_stack),
            "sorted_list": list(sorted_list)
        })

        for v in graph.get_adj_list()[u]:
            if cycle_detected: # Stop if cycle already found
                break
            if visited[v] == 0: # If not visited, recurse
                steps.append({
                    "type": "dfs_explore_edge",
                    "message": f"Exploring edge {u} -> {v}. {v} is unvisited, continuing DFS.",
                    "current_node": u,
                    "target_node": v,
                    "visited_status": dict(visited),
                    "recursion_stack": dict(recursion_stack),
                    "sorted_list": list(sorted_list)
                })
                dfs_util(v)
            elif recursion_stack[v]: # If v is in current recursion stack, it's a back-edge -> cycle!
                cycle_detected = True
                steps.append({
                    "type": "cycle_detected",
                    "message": f"Back-edge detected {u} -> {v}. Cycle found!",
                    "current_node": u,
                    "target_node": v,
                    "visited_status": dict(visited),
                    "recursion_stack": dict(recursion_stack),
                    "sorted_list": list(sorted_list)
                })
                return

        recursion_stack[u] = False # Remove from recursion stack
        visited[u] = 2 # Mark as visited
        sorted_list.append(u) # Add to sorted list (in reverse order for topological sort)
        steps.append({
            "type": "dfs_finish_node",
            "message": f"Finished processing node {u}. Adding {u} to sorted list.",
            "current_node": u,
            "visited_status": dict(visited),
            "recursion_stack": dict(recursion_stack),
            "sorted_list": list(sorted_list)
        })

    # Call DFS for all unvisited vertices
    for v in graph.get_vertices():
        if visited[v] == 0 and not cycle_detected:
            dfs_util(v)
        if cycle_detected:
            break

    if cycle_detected:
        steps.append({
            "type": "final_result",
            "message": "Topological sort failed due to cycle detection.",
            "sorted_list": [],
            "cycle_detected": True
        })
        return [], True, steps
    else:
        # Reverse the list for correct topological order
        final_sorted_list = sorted_list[::-1]
        steps.append({
            "type": "final_result",
            "message": "Topological sort completed successfully.",
            "sorted_list": list(final_sorted_list),
            "cycle_detected": False
        })
        return final_sorted_list, False, steps


# Example Usage (for testing purposes, not part of Streamlit app)
if __name__ == "__main__":
    print("--- Testing Kahn's Algorithm ---")
    g_kahn = Graph()
    g_kahn.add_edge("A", "B")
    g_kahn.add_edge("A", "C")
    g_kahn.add_edge("B", "D")
    g_kahn.add_edge("C", "D")
    g_kahn.add_edge("E", "F") # Isolated component

    sorted_kahn, has_cycle_kahn, kahn_steps = topological_sort_kahn(g_kahn)
    print(f"Kahn's Sorted Order: {sorted_kahn}")
    print(f"Kahn's Cycle Detected: {has_cycle_kahn}")
    # print("\nKahn's Steps:")
    # for i, step in enumerate(kahn_steps):
    #     print(f"Step {i+1}: {step['message']} - Sorted: {step['sorted_list']}")

    print("\n--- Testing Kahn's Algorithm with Cycle ---")
    g_kahn_cycle = Graph()
    g_kahn_cycle.add_edge("A", "B")
    g_kahn_cycle.add_edge("B", "C")
    g_kahn_cycle.add_edge("C", "A") # Cycle
    sorted_kahn_cycle, has_cycle_kahn_cycle, kahn_cycle_steps = topological_sort_kahn(g_kahn_cycle)
    print(f"Kahn's Cycle Sorted Order: {sorted_kahn_cycle}")
    print(f"Kahn's Cycle Detected: {has_cycle_kahn_cycle}")

    print("\n--- Testing DFS Algorithm ---")
    g_dfs = Graph()
    g_dfs.add_edge("A", "B")
    g_dfs.add_edge("A", "C")
    g_dfs.add_edge("B", "D")
    g_dfs.add_edge("C", "D")
    g_dfs.add_edge("E", "F") # Isolated component

    sorted_dfs, has_cycle_dfs, dfs_steps = topological_sort_dfs(g_dfs)
    print(f"DFS Sorted Order: {sorted_dfs}")
    print(f"DFS Cycle Detected: {has_cycle_dfs}")
    # print("\nDFS Steps:")
    # for i, step in enumerate(dfs_steps):
    #     print(f"Step {i+1}: {step['message']} - Sorted: {step['sorted_list']}")

    print("\n--- Testing DFS Algorithm with Cycle ---")
    g_dfs_cycle = Graph()
    g_dfs_cycle.add_edge("X", "Y")
    g_dfs_cycle.add_edge("Y", "Z")
    g_dfs_cycle.add_edge("Z", "X") # Cycle
    sorted_dfs_cycle, has_cycle_dfs_cycle, dfs_cycle_steps = topological_sort_dfs(g_dfs_cycle)
    print(f"DFS Cycle Sorted Order: {sorted_dfs_cycle}")
    print(f"DFS Cycle Detected: {has_cycle_dfs_cycle}")