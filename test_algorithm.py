# test_algorithm.py

import unittest
from algorithm import Graph, topological_sort_kahn, topological_sort_dfs

class TestTopologicalSort(unittest.TestCase):

    def test_kahn_simple_dag(self):
        """Test Kahn's algorithm with a simple Directed Acyclic Graph (DAG)."""
        graph = Graph()
        graph.add_edge("A", "B")
        graph.add_edge("A", "C")
        graph.add_edge("B", "D")
        graph.add_edge("C", "D")
        sorted_list, cycle_detected, _ = topological_sort_kahn(graph)
        
        self.assertFalse(cycle_detected)
        # Multiple valid topological sorts exist, check if it's one of them
        # (A, C, B, D) or (A, B, C, D) are valid
        self.assertTrue(sorted_list == ["A", "B", "C", "D"] or sorted_list == ["A", "C", "B", "D"])
        
    def test_kahn_complex_dag(self):
        """Test Kahn's algorithm with a more complex DAG."""
        graph = Graph()
        graph.add_edge("A", "B")
        graph.add_edge("A", "C")
        graph.add_edge("B", "D")
        graph.add_edge("C", "E")
        graph.add_edge("D", "F")
        graph.add_edge("E", "F")
        graph.add_edge("G", "H") # Disconnected component
        graph.add_edge("G", "I")
        graph.add_edge("H", "J")
        graph.add_edge("I", "J")
        
        sorted_list, cycle_detected, _ = topological_sort_kahn(graph)
        self.assertFalse(cycle_detected)
        self.assertEqual(len(sorted_list), graph.num_vertices) # All nodes should be processed
        # A more robust check for validity: ensure no edge goes from a later node to an earlier one
        for u in sorted_list:
            for v in graph.get_adj_list()[u]:
                self.assertLess(sorted_list.index(u), sorted_list.index(v), f"Edge {u}->{v} violates topological order.")


    def test_kahn_graph_with_cycle(self):
        """Test Kahn's algorithm with a graph containing a cycle."""
        graph = Graph()
        graph.add_edge("A", "B")
        graph.add_edge("B", "C")
        graph.add_edge("C", "A") # Cycle A -> B -> C -> A
        sorted_list, cycle_detected, _ = topological_sort_kahn(graph)
        self.assertTrue(cycle_detected)
        self.assertNotEqual(len(sorted_list), graph.num_vertices) # Not all nodes can be processed

    def test_kahn_empty_graph(self):
        """Test Kahn's algorithm with an empty graph."""
        graph = Graph()
        sorted_list, cycle_detected, _ = topological_sort_kahn(graph)
        self.assertFalse(cycle_detected)
        self.assertEqual(sorted_list, [])
        self.assertEqual(graph.num_vertices, 0)

    def test_kahn_single_node_graph(self):
        """Test Kahn's algorithm with a graph containing a single isolated node."""
        graph = Graph()
        graph.add_edge("A", "A") # Self-loop (technically a cycle)
        sorted_list, cycle_detected, _ = topological_sort_kahn(graph)
        self.assertTrue(cycle_detected) # Self-loop is a cycle

        graph_no_edge = Graph()
        graph_no_edge.add_edge("A", "B") # Add one edge to establish nodes, then remove
        graph_no_edge = Graph() # Re-initialize for just a node
        graph_no_edge.add_edge('X', 'Y') # Dummy edge to add X and Y
        graph_no_edge.adj.pop('Y', None) # Remove Y's entry if no outgoing
        graph_no_edge.adj.pop('X', None) # Remove X's entry if no outgoing
        
        # A better way to add a single isolated node:
        # For current Graph class, a node is added implicitly by add_edge.
        # If we want a standalone node 'A' without edges, Graph(1) would conceptually work
        # but our add_edge is how nodes get into self.vertices.
        # Let's adjust Graph class slightly or test with nodes that are implicitly added/removed.
        # For now, test the implicit adding by only adding one edge and then using that node.
        graph_single_node = Graph()
        graph_single_node.add_edge("P", "Q")
        graph_single_node.adj = defaultdict(list) # Clear edges to make P & Q isolated
        graph_single_node.indegree = defaultdict(int)
        
        # Manually ensure P and Q are in vertices list for Kahn's
        graph_single_node.vertices.add("P")
        graph_single_node.vertices.add("Q")
        graph_single_node.num_vertices = 2

        sorted_list, cycle_detected, _ = topological_sort_kahn(graph_single_node)
        self.assertFalse(cycle_detected)
        self.assertIn("P", sorted_list)
        self.assertIn("Q", sorted_list)
        self.assertEqual(len(sorted_list), 2)


    def test_dfs_simple_dag(self):
        """Test DFS-based algorithm with a simple DAG."""
        graph = Graph()
        graph.add_edge("A", "B")
        graph.add_edge("A", "C")
        graph.add_edge("B", "D")
        graph.add_edge("C", "D")
        sorted_list, cycle_detected, _ = topological_sort_dfs(graph)
        self.assertFalse(cycle_detected)
        self.assertTrue(sorted_list == ["A", "C", "B", "D"] or sorted_list == ["A", "B", "C", "D"])

    def test_dfs_complex_dag(self):
        """Test DFS-based algorithm with a more complex DAG."""
        graph = Graph()
        graph.add_edge("A", "B")
        graph.add_edge("A", "C")
        graph.add_edge("B", "D")
        graph.add_edge("C", "E")
        graph.add_edge("D", "F")
        graph.add_edge("E", "F")
        graph.add_edge("G", "H") # Disconnected component
        graph.add_edge("G", "I")
        graph.add_edge("H", "J")
        graph.add_edge("I", "J")
        
        sorted_list, cycle_detected, _ = topological_sort_dfs(graph)
        self.assertFalse(cycle_detected)
        self.assertEqual(len(sorted_list), graph.num_vertices)
        for u in sorted_list:
            for v in graph.get_adj_list()[u]:
                self.assertLess(sorted_list.index(u), sorted_list.index(v), f"Edge {u}->{v} violates topological order.")


    def test_dfs_graph_with_cycle(self):
        """Test DFS-based algorithm with a graph containing a cycle."""
        graph = Graph()
        graph.add_edge("X", "Y")
        graph.add_edge("Y", "Z")
        graph.add_edge("Z", "X") # Cycle X -> Y -> Z -> X
        sorted_list, cycle_detected, _ = topological_sort_dfs(graph)
        self.assertTrue(cycle_detected)
        self.assertEqual(len(sorted_list), 0) # No topological sort possible if cycle detected

    def test_dfs_empty_graph(self):
        """Test DFS-based algorithm with an empty graph."""
        graph = Graph()
        sorted_list, cycle_detected, _ = topological_sort_dfs(graph)
        self.assertFalse(cycle_detected)
        self.assertEqual(sorted_list, [])
        self.assertEqual(graph.num_vertices, 0)
    
    def test_dfs_single_node_graph(self):
        """Test DFS-based algorithm with a graph containing a single isolated node."""
        graph = Graph()
        graph.add_edge("P", "Q") # Dummy edge to add nodes P and Q
        graph.adj = defaultdict(list) # Clear edges to make P & Q isolated
        graph.indegree = defaultdict(int)
        
        # Manually ensure P and Q are in vertices list for DFS
        graph.vertices.add("P")
        graph.vertices.add("Q")
        graph.num_vertices = 2

        sorted_list, cycle_detected, _ = topological_sort_dfs(graph)
        self.assertFalse(cycle_detected)
        self.assertIn("P", sorted_list)
        self.assertIn("Q", sorted_list)
        self.assertEqual(len(sorted_list), 2)


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False) # Allows running in IDE/console without issues
