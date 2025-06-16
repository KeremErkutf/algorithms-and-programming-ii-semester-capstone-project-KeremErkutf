# Topological Sort Algorithm Description

## 📌 Introduction to Topological Sort

**Topological Sort** is a linear ordering of vertices in a **Directed Acyclic Graph (DAG)** such that for every directed edge `U → V`, vertex `U` comes before vertex `V` in the ordering.

🔒 **Important:** Topological sort is **only possible for DAGs**. If the graph contains a cycle, a topological sort cannot be performed.

### 🔧 Applications of Topological Sorting

- **Task Scheduling**: Where some tasks must be completed before others (e.g., Makefiles).
- **Course Scheduling**: For handling prerequisites in university courses.
- **Dependency Resolution**: In package managers or data pipelines.

➡️ *Note: For a given DAG, there may be multiple valid topological orders.*

---

## 🧮 Common Algorithms for Topological Sort

### 1. Kahn’s Algorithm (BFS-based)

**Kahn’s Algorithm** is an iterative, BFS-like method that processes vertices with **zero in-degree** (no prerequisites).

#### 🧠 Working Principle

1. **Calculate In-Degrees**:
   - Compute in-degree for every vertex (number of incoming edges).

2. **Initialize Queue**:
   - Add all vertices with in-degree `0` to a queue.

3. **Process Vertices**:
   - While the queue is not empty:
     - Dequeue vertex `u` and add it to the result list.
     - For each neighbor `v` of `u`:
       - Decrement `v`'s in-degree.
       - If `v`'s in-degree becomes `0`, enqueue `v`.

4. **Cycle Detection**:
   - If the number of processed vertices < total vertices → cycle exists.
   - Remaining vertices with non-zero in-degrees form the cycle.

#### ⏱️ Complexity Analysis

| Operation | Time Complexity | Space Complexity |
|-----------|------------------|------------------|
| In-degree computation | O(V + E) | O(V) |
| Queue operations | O(V) | O(V) |
| Edge processing | O(E) | O(E) |
| **Total** | **O(V + E)** | **O(V + E)** |

---

### 2. DFS-based Algorithm

This algorithm uses **Depth-First Search** (DFS) and adds each vertex to the sort after all its descendants have been visited.

#### 🧠 Working Principle

1. **Visited States**:
   - `0`: Unvisited
   - `1`: Visiting (in recursion stack)
   - `2`: Visited

2. **DFS Traversal**:
   - For each unvisited vertex:
     - Mark as Visiting.
     - For each neighbor:
       - If Unvisited → recursive DFS call.
       - If Visiting → cycle detected.
     - After processing, mark as Visited and push to stack.

3. **Final Order**:
   - Reverse the stack to obtain topological sort.

#### ⏱️ Complexity Analysis

| Operation | Time Complexity | Space Complexity |
|-----------|------------------|------------------|
| Vertex + edge traversal | O(V + E) | O(V + E) |
| Visited map | — | O(V) |
| Call stack (recursion) | — | O(V) |
| **Total** | **O(V + E)** | **O(V + E)** |

---

## ⚠️ Handling Cycles

Both algorithms can detect cycles:

- **Kahn’s Algorithm**:  
  - If processed vertex count < total vertex count → cycle detected.

- **DFS-based Algorithm**:  
  - If during DFS, you revisit a vertex marked as *Visiting* → cycle detected.

In such cases, the algorithm should report:
