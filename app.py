# app.py

import streamlit as st

def main():
    """
    Main function to run the Streamlit application.
    """
    st.set_page_config(page_title="Topological Sort Visualizer", layout="wide")
    st.title("Topological Sort Algorithm Visualizer")
    st.write("Welcome to the Semester Capstone Project for Algorithms and Programming II!")
    st.write("This application will allow you to visualize and understand the Topological Sort algorithm.")

    st.sidebar.header("About")
    st.sidebar.info(
        "This project implements and visualizes the Topological Sort algorithm. "
        "It's part of the Algorithms and Programming II course at Fırat University."
    )
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Assoc. Prof. Ferhat UÇAR**")
    st.sidebar.markdown("April 2025 - June 2025")

if __name__ == "__main__":
    main()
