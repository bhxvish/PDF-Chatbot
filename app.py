import streamlit as st
from utils import extract, chunk, store, query
st.title("CHAT WITH YOUR PDF")
uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file:
    with st.spinner("Reading your PDF....."):
        text = extract(uploaded_file)
        chunks = chunk(text)
        index, embeddings, chunk_list = store(chunks)
        st.success("PDF processed. Ask a question below")
        user_query = st.text_input("Enter your question: ")
        if user_query:
            with st.spinner("Searching..."):
                results = query(user_query, index, chunk_list)
                for i in results:
                    st.write(i)