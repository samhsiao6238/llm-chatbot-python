import streamlit as st
from langchain_community.graphs import Neo4jGraph
# import os

graph = Neo4jGraph(
    url=st.secrets["NEO4J_URI"],
    username=st.secrets["NEO4J_USERNAME"],
    password=st.secrets["NEO4J_PASSWORD"],
    # url=os.getenv("NEO4J_URI"),
    # username=os.getenv("NEO4J_USERNAME"),
    # password=os.getenv("NEO4J_PASSWORD"),    
)
