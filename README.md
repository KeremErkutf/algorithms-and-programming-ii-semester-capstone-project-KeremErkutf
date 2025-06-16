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
project-repository/
├── app.py                  # Main Streamlit application
├── algorithm.py            # Implementation of Graph class and topological sort algorithms
├── utils.py                # Helper functions (currently empty, for future use)
├── visualizer.py           # Visualization components (graph drawing)
├── README.md               # Project documentation (this file)
├── requirements.txt        # List of required Python packages
├── test_algorithm.py       # Unit tests for the algorithm implementations
└── data/                   # (Optional) Folder for sample data files if applicable
└── (e.g., default_graph.json)
└── docs/                   # (Optional) Additional documentation or screenshots
└── screenshots/
├── screenshot1.png # Placeholder for application screenshots
└── screenshot2.png

---

## Installation and Usage

To set up and run this project locally, follow these steps:

1.  **Clone Your Repository:**
    ```bash
    git clone [YOUR_GITHUB_REPO_URL] 
    cd your-project-repository # Replace with your actual repository folder name
    ```

2.  **Create a Virtual Environment:**
    ```bash
    python -m venv venv
    ```

3.  **Activate the Virtual Environment:**
    * **On Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
    * **On macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```

4.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    (Note: The `requirements.txt` file is generated after the initial setup. Ensure it contains `streamlit`, `networkx`, and `matplotlib`.)

5.  **Run the Streamlit Application:**
    ```bash
    streamlit run app.py
    ```
    This will open the application in your default web browser (usually at `http://localhost:8501`).

6.  **Run Unit Tests (Optional):**
    To ensure the algorithms are working correctly, you can run the unit tests:
    ```bash
    python -m unittest test_algorithm.py
    ```

---

## Deployment

**Streamlit web-app address (URL to your deployed application):**
[TO BE ADDED AFTER DEPLOYMENT]

**Instructions:**
1.  Create a free account on [Streamlit Cloud](https://streamlit.io/cloud).
2.  Connect your GitHub repository to Streamlit Cloud.
3.  Select the `main` (or `master`) branch and `app.py` as your main file.
4.  Deploy your application.
5.  Once deployed, copy the URL and paste it here.

---

## Screenshots

*(Placeholder for screenshots of the application. Add compelling images here once your app is fully functional and deployed.)*

---

## Complexity Analysis

### Kahn's Algorithm (BFS-based)
-   **Time Complexity:** $O(V + E)$
    -   Where $V$ is the number of vertices and $E$ is the number of edges.
    -   Each vertex is added to the queue and processed at most once. Each edge is visited exactly once when updating indegrees.
-   **Space Complexity:** $O(V + E)$
    -   This accounts for storing the adjacency list, the indegree array, and the queue.

### DFS-based Algorithm
-   **Time Complexity:** $O(V + E)$
    -   Where $V$ is the number of vertices and $E$ is the number of edges.
    -   Each vertex and each edge are visited exactly once during the Depth-First Search.
-   **Space Complexity:** $O(V + E)$
    -   This accounts for storing the adjacency list, the visited array, and the recursion stack (which can go up to $O(V)$ in the worst case for a deeply nested path).

---

## References and Resources

-   Streamlit Documentation: [https://docs.streamlit.io](https://docs.streamlit.io)
-   NetworkX Documentation: [https://networkx.org/documentation/stable/](https://networkx.org/documentation/stable/)
-   Matplotlib Documentation: [https://matplotlib.org/stable/contents.html](https://matplotlib.org/stable/contents.html)
-   Introduction to Algorithms (CLRS) - 4th Edition
-   Algorithm Design Manual - Steven Skiena
-   VisuAlgo: [https://visualgo.net](https://visualgo.net) (for algorithm visualization concepts)

---

