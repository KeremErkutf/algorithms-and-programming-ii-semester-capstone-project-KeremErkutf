# Algorithms and Programming II - Semester Capstone Project: Topological Sort Visualization

## Overview

Welcome to the Algorithms and Programming II course project at Fırat University, Technology Faculty, Software Engineering Department. This project involves developing an interactive web application to implement, visualize, and analyze the **Topological Sort Algorithm** using Python and Streamlit.

## Learning Objectives

This project is designed to help me:

* Implement the Topological Sort algorithm in Python
* Create interactive visualizations that demonstrate algorithm behavior
* Analyze and understand the time and space complexity of the algorithm
* Practice modern software development workflows using Git and GitHub
* Gain experience with web application development and deployment
* Improve technical documentation skills

## Technology Stack

* **Programming Language:** Python 3.8+
* **Web Framework:** Streamlit
* **Version Control:** Git and GitHub
* **Deployment:** Streamlit Cloud

## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

* Python 3.8 or higher
* Git
* A GitHub account
* A text editor or IDE (e.g., VS Code, PyCharm)

### Setting Up Your Development Environment

1.  **Accept the GitHub Classroom Assignment:**
    * Click on the assignment link provided by the instructor.
    * This will create a personal copy of the project template in your GitHub account.

2.  **Clone Your Repository:**

    ```bash
    git clone [YOUR_GITHUB_REPO_URL] # Kendi GitHub repo URL'ni buraya yapıştır
    cd your-project-repo
    ```

3.  **Create a Virtual Environment:**

    ```bash
    # On Windows
    python -m venv venv
    venv\Scripts\activate

    # On macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

4.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Project Requirements (Topological Sort Specific)

### Algorithm Implementation

* Correctly implement the Topological Sort algorithm (e.g., Kahn's Algorithm or DFS-based).
* Handle various graph structures including disconnected components and graphs with cycles (and detect/handle cycles appropriately).

### Interactive Interface

* Allow users to define custom directed acyclic graphs (DAGs) (e.g., node count, edge definitions).
* Provide controls to trigger the sorting process and step through the algorithm.

### Visualization

* Clearly visualize the graph structure (nodes, directed edges).
* Highlight nodes and edges as the topological sort algorithm progresses.
* Show the sorted order being built up.

### Step-by-Step Explanation

* Provide a textual explanation for each major step of the algorithm's execution during visualization.
* Explain which node is being processed, why, and how the sorted list is updated.

### Complexity Analysis

* Document the time and space complexity of Topological Sort using Big O notation for different implementations (e.g., adjacency list vs. adjacency matrix).
* Explain how the complexity relates to the number of vertices (V) and edges (E).

### Test Cases

* Include examples of various DAGs (simple, complex, empty, single-node).
* Demonstrate cycle detection and how the algorithm handles graphs with cycles (it cannot perform topological sort on cyclic graphs).

## Repository Structure
project-repository/
├── app.py                     # Main Streamlit application
├── algorithm.py               # Implementation of your algorithm
├── utils.py                   # Helper functions
├── visualizer.py              # Visualization components
├── README.md                  # Project documentation
├── requirements.txt           # Python package dependencies
├── test_algorithm.py          # Unit tests
├── examples/                  # Example inputs and outputs
│   └── (e.g., example_graph.json)
├── data/                      # Sample data files (if applicable, e.g., default graphs)
│   └── (e.g., default_graph.json)
└── docs/                      # Additional documentation
├── algorithm_description.md
└── screenshots/
├── screenshot1.png
└── screenshot2.png

## Documentation Requirements

Your `README.md` will be continuously updated to include:

* Project title and description
* Algorithm explanation with mathematical notation when appropriate
* Installation and usage instructions
* Screenshots of the application (once developed)
* Complexity analysis with explanations
* Examples of inputs and outputs
* Known limitations and future improvements
* References and resources used
* Streamlit web-app address (URL to your deployed application - to be added later)

## Deployment Instructions

(To be filled in later once the application is ready for deployment)

## Evaluation Criteria

(As per the project document)

## Submission Guidelines

(As per the project document)

## Resources

(As per the project document)

## Contact Information

(As per the project document)