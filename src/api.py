# src/api.py
from fastapi import FastAPI
from pydantic import BaseModel
import os

# These imports depend on your project files existing:
# - src/retriever.py must expose a `retrieve(query, top_k=...)` function
# - src/prompt_utils.py must expose `generate_with_openai` and `fallback_summarize`
# If those modules raise import errors, we'll surface them when you run the import-check.
from src.retriever import retrieve
from src.prompt_utils import generate_with_openai, fallback_summarize

app = FastAPI(title="Fast RAG Lite API")

class Query(BaseModel):
    query: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/query")
def query_endpoint(q: Query):
    # Retrieve relevant contexts
    contexts = retrieve(q.query, top_k=5)

    # Try LLM generation if OpenAI key available, otherwise fallback
    openai_key = os.getenv("OPENAI_API_KEY")
    answer = None
    if openai_key:
        try:
            answer = generate_with_openai(q.query, contexts, openai_key)
        except Exception:
            # if generation failed for any reason, fall back to deterministic summary
            answer = None

    if not answer:
        answer = fallback_summarize(q.query, contexts)

    sources = [c.get("source") for c in contexts]
    return {"answer": answer, "sources": sources}
