# src/prompt_utils.py
import os
from typing import List, Optional

def generate_with_openai(query: str, contexts: List[dict], openai_key: Optional[str] = None, model: str = "gpt-4o-mini-instruct", max_tokens: int = 300):
    """
    Lazy-imports openai and calls ChatCompletion.
    Returns the generated answer string, or raises if generation failed.
    If openai_key is None, raises ImportError to signal the caller.
    """
    if openai_key is None:
        raise ValueError("OpenAI key not provided")

    try:
        import openai
    except Exception as e:
        # make the error explicit and easy to handle by caller
        raise ImportError("openai package is not installed") from e

    openai.api_key = openai_key

    # keep contexts small to avoid huge prompts
    context_text = "\n\n---\n\n".join([c.get("text","")[:1500] for c in contexts])
    prompt = (
        "You are an expert assistant. Use the following document contexts to answer the user query concisely and accurately.\n\n"
        f"Contexts:\n{context_text}\n\n"
        f"Query: {query}\n\n"
        "Provide a short precise answer and cite the source filename for any fact taken from the documents. "
        "If the answer is not in the contexts, reply: 'Insufficient information in documents.'"
    )

    # Use ChatCompletion if available, fallback to Chat API shape
    try:
        # prefer ChatCompletion if available
        resp = openai.ChatCompletion.create(
            model=model,
            messages=[{"role":"user","content":prompt}],
            max_tokens=max_tokens,
            temperature=0.0
        )
        return resp["choices"][0]["message"]["content"].strip()
    except AttributeError:
        # older/openai versions might use different API shapes; try a safe fallback
        resp = openai.Completion.create(
            model=model,
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=0.0
        )
        return resp["choices"][0]["text"].strip()

def fallback_summarize(query: str, contexts: List[dict]) -> str:
    """
    Deterministic fallback if no LLM is available.
    Concatenates trimmed top contexts and labels them - useful for offline demos.
    """
    if not contexts:
        return "No documents loaded."

    top_texts = []
    for c in contexts[:5]:
        src = c.get("source", "unknown")
        txt = c.get("text", "")[:800].replace("\n", " ")
        top_texts.append(f"[{src}] {txt}")

    joined = "\n\n".join(top_texts)
    return f"Top contexts (deterministic fallback):\n\n{joined}\n\n(Use OPENAI_API_KEY to enable LLM generation.)"
