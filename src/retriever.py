# src/retriever.py
from src.embed import embed_texts
from src.indexer import search
import numpy as np

def retrieve(query, top_k=5):
    q_emb = embed_texts([query])
    D,I,meta = search(q_emb, k=top_k)
    results=[]
    for idx in I[0]:
        results.append(meta[idx])
    return results
