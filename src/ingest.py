# src/ingest.py
import os, glob, json
from pathlib import Path
from tqdm import tqdm
import PyPDF2

def extract_text(path):
    text = ""
    with open(path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def chunk_text(text, chunk_size=800, overlap=100):
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)
        i += chunk_size - overlap
    return chunks

def run(pdf_folder="documents", out_json="data/chunks.json"):
    Path("data").mkdir(exist_ok=True)

    all_chunks = []
    pdfs = glob.glob(os.path.join(pdf_folder, "*.pdf"))

    print("PDFs found:", pdfs)

    for pdf in pdfs:
        print("Processing:", pdf)
        txt = extract_text(pdf)

        if len(txt.strip()) == 0:
            print("⚠ WARNING: No text extracted from:", pdf)

        chunks = chunk_text(txt)

        for c in chunks:
            all_chunks.append({"source": os.path.basename(pdf), "text": c})

    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, ensure_ascii=False)

    print(f"Saved {len(all_chunks)} chunks -> {out_json}")

if __name__ == "__main__":
    run()
