# Algorithms and Programming II: Semester Capstone Project - Topological Sort Visualization

## Introduction

Welcome to the semester capstone project for Algorithm and Programming II at Fırat University's Technology Faculty, Software Engineering Department. This project is an interactive web application that implements, visualizes, and analyzes the **Topological Sort Algorithm** using Python and Streamlit.

This application is designed to enhance understanding of topological sorting through practical implementation, clear visualization, and detailed analysis, while also building valuable skills in software development, web application deployment, and technical documentation.

---

## Project Overview

### Objectives
- Implement the Topological Sort algorithm (Kahn's and DFS-based) using Python.
- Create interactive visualizations that demonstrate how the algorithm operates step-by-step.
- Analyze and document the time and space complexity of the algorithm using Big O notation.
- Provide clear documentation explaining the algorithm's working principles.
- Deploy a functioning Streamlit application for public access.

### Technology Stack
- **Programming Language:** Python 3.8+
- **Web Framework:** Streamlit
- **Visualization Libraries:** NetworkX, Matplotlib
- **Version Control:** Git and GitHub
- **Deployment:** Streamlit Cloud

---

## Project Requirements (Topological Sort Specific)

### Algorithm Implementation
- Correct and efficient implementation of both **Kahn's Algorithm (BFS-based)** and **DFS-based Topological Sort**.
- Ability to handle various graph structures, including disconnected components.
- **Cycle detection:** The application can identify and report cycles in the graph, indicating that a topological sort is not possible.

### Interactive Interface
- Users can define custom directed acyclic graphs (DAGs) by entering edges.
- Provides **pre-defined example graphs** to quickly demonstrate different scenarios (simple, complex, cyclic, disconnected).
- User controls (slider) to step through the algorithm's execution and observe its state changes.

### Visualization
- Clear visualization of the graph structure (nodes, directed edges) using `networkx` and `matplotlib`.
- **Dynamic highlighting** of nodes and edges as the topological sort algorithm progresses (e.g., current node, nodes in queue/recursion stack, visited nodes).
- Visual indication of the sorted order being built up.

### Step-by-Step Explanation
- A textual walkthrough feature displays detailed explanations for each major stage of the algorithm's execution, including current node processing, queue/stack status, and indegree updates.

### Complexity Analysis
- Documentation of both time and space complexity using Big O notation for both Kahn's and DFS-based algorithms.
- Explanations of how these measures relate to the number of vertices ($V$) and edges ($E$).

### Test Cases
- Includes a dedicated unit test file (`test_algorithm.py`) with a variety of examples demonstrating the algorithm's behavior under different conditions, including simple DAGs, complex DAGs, cyclic graphs, empty graphs, and single-node/disconnected graphs.

---

## Repository Structure