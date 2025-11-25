# src/embed.py
from sentence_transformers import SentenceTransformer
import numpy as np

MODEL_NAME = "all-MiniLM-L6-v2"

_model = None
def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    return _model

def embed_texts(texts):
    model = get_model()
    emb = model.encode(texts, show_progress_bar=False, convert_to_numpy=True)
    return emb.astype("float32")
