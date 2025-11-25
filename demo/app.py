# demo/app.py
import streamlit as st
import requests, os

st.title("Fast RAG Lite — Local RAG Demo")
api_url = st.text_input("API URL (e.g. http://localhost:8000)", value="http://localhost:8000")
q = st.text_input("Ask about the documents")
if st.button("Search"):
    try:
        r = requests.post(f"{api_url}/query", json={"query": q}, timeout=20)
        data = r.json()
        st.markdown("**Answer:**")
        st.write(data["answer"])
        st.markdown("**Sources:**")
        for s in data["sources"]:
            st.write("-", s)
    except Exception as e:
        st.error(f"Query failed: {e}")
