import fitz
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
model = SentenceTransformer("all-MiniLM-L6-v2")

def extract(pdf_file):
    doc = fitz.open(stream= pdf_file.read(), filetype="pdf")
    text = ""
    for i in doc:
        text += i.get_text()
    return text

def chunk(text, chunk_size=500):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def store(chunks):
    embeddings = model.encode(chunks)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings))
    return index, embeddings, chunks

def query(query, index, chunks, k=3):
    query_vec = model.encode([query])
    dist, indices = index.search(query_vec, k)
    return [chunks[i] for i in indices[0]]