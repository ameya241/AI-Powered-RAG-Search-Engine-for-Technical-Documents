# src/indexer.py
import faiss, numpy as np, json
from pathlib import Path

META_PATH = "data/chunks.json"
INDEX_PATH = "data/faiss.index"
META_OUT = "data/meta.json"

def build_index():
    import json
    from src.embed import embed_texts
    chunks = json.load(open(META_PATH, "r", encoding="utf-8"))
    texts = [c["text"] for c in chunks]
    embs = embed_texts(texts)
    dim = embs.shape[1]
    index = faiss.IndexFlatIP(dim)
    faiss.normalize_L2(embs)
    index.add(embs)
    Path("data").mkdir(exist_ok=True)
    faiss.write_index(index, INDEX_PATH)
    with open(META_OUT, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False)
    print("Index and metadata saved.")

def load_index():
    index = faiss.read_index(INDEX_PATH)
    meta = json.load(open(META_OUT,"r",encoding="utf-8"))
    return index, meta

def search(query_emb, k=5):
    index, meta = load_index()
    faiss.normalize_L2(query_emb)
    D, I = index.search(query_emb, k)
    return D, I, meta
