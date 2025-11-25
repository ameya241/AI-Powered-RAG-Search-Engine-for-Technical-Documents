# AI-Powered-RAG-Search-Engine-for-Technical-Documents
<h1>✨ Project Overview</h1>

Fast RAG Lite is a lightweight, easy-to-understand AI system that shows how real-world Retrieval-Augmented Generation (RAG) works.

<h3>The goal was simple:</h3>

📄 Give the system a PDF (for example, my own resume)
🔍 Let it read and break the text into small chunks
🧠 Convert those chunks into embeddings
🎯 Search for the most relevant pieces when a question is asked
💬 Return an answer based only on the document content

Even if there is no OpenAI API key, the system still works.
It uses a deterministic fallback mode that summarizes the most relevant chunks, so it always produces an answer.

If an OpenAI key is available, it automatically switches to a smarter, natural-language response powered by an LLM.

<h2>🚀 Why I Built This</h2>

This project helped me understand:

How PDFs are processed in real applications

How embeddings represent text numerically

How vector similarity search finds relevant information

How to build an end-to-end RAG pipeline

How to expose everything through a clean FastAPI backend

The result is a clear, functional, and production-style RAG system that is easy to understand but still demonstrates real AI engineering skills.

<h2>📌 Bonus: Real-World Proof</h2>

The system includes my resume for testing:

/mnt/data/Ameya Ajay-Jadhav.pdf

You can ask the API questions about it, and it will answer using retrieval.






