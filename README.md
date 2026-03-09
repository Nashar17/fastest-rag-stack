# Fastest RAG Stack

A fully local Retrieval-Augmented Generation (RAG) backend built using **ChromaDB, FastAPI, and LLMs (Ollama + Llama2)**.

This project implements a complete RAG pipeline that ingests PDF documents, embeds them into a vector database, and answers natural language questions using only the content of the provided documents.

> "What is attention in transformers?"

and returns a grounded, context-aware answer generated entirely locally — no OpenAI, no cloud, no cost.

---

## Features

- PDF ingestion and text extraction
- Text chunking with configurable size and overlap
- Semantic embeddings using `nomic-embed-text`
- Vector storage and similarity search using `ChromaDB`
- LLM-generated answers using `llama2`
- Fully local — no API keys required
- Clean modular architecture
- FastAPI REST API with Swagger UI

---

## System Architecture

```
PDF Documents
⬇
PDF Loader (pypdf)
⬇
Text Chunker
⬇
Embedding Model (nomic-embed-text)
⬇
ChromaDB Vector Store
⬇
Retriever (Similarity Search)
⬇
Prompt Construction
⬇
LLM Generation (llama2)
⬇
Final Answer
```

---

## Project Structure

```
fastest-rag-stack/
│
├── app/
│   ├── ingestion/
│   │   ├── pdf_loader.py
│   │   ├── text_chunker.py
│   │   └── embedding_generator.py
│   │
│   ├── retrieval/
│   │   ├── vector_store.py
│   │   └── retriever.py
│   │
│   ├── generation/
│   │   └── llm_generator.py
│   │
│   ├── config.py
│   └── main.py
│
├── data/
│   └── pdfs/
│
├── requirements.txt
└── README.md
```

---

## Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/Nashar17/fastest-rag-stack.git
cd fastest-rag-stack
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Install Ollama

Download from: https://ollama.com

Pull required models:

```bash
ollama pull nomic-embed-text
ollama pull llama2
```

### 5️⃣ Add your PDF files

Place your PDF documents inside the `data/pdfs/` folder.

### 6️⃣ Run the API

```bash
python -m uvicorn app.main:app --reload
```

Open Swagger UI:
```
http://127.0.0.1:8000/docs
```

---

## API Endpoints

### `POST /ingest`
Load all PDFs from `data/pdfs/`, chunk, embed, and store in ChromaDB.
Call this once before querying.

```json
Response:
{
  "status": "Ingestion complete",
  "documents_loaded": 3,
  "chunks_created": 120,
  "embeddings_stored": 120
}
```

---

### `GET /retrieve?query=...&k=3`
Retrieve the top k most relevant chunks for a query.

```
GET /retrieve?query=What is attention in transformers?&k=3
```

---

### `GET /ask?query=...`
Full RAG pipeline — retrieves relevant chunks and generates a grounded answer.

```
GET /ask?query=What is attention in transformers?
```

```json
Response:
{
  "query": "What is attention in transformers?",
  "answer": "Attention in transformers is a mechanism that...",
  "retrieved_chunks": [...]
}
```

---

## Design Decisions

**Why ChromaDB?**
Lightweight, fully local vector database — no external services needed, perfect for local RAG pipelines.

**Why nomic-embed-text?**
High quality open-source embedding model that runs locally via Ollama with no API costs.

**Why LLM After Retrieval?**
To generate natural, context-aware answers instead of returning raw document chunks to the user.

**Why Separate Ingest / Retrieve / Ask endpoints?**
Clean separation of concerns — ingest once, query many times. Makes debugging and testing each stage independently much easier.

---

## Future Improvements

- Persistent ChromaDB storage across server restarts
- Support for multiple file types (`.txt`, `.docx`, `.md`)
- Streaming LLM responses
- Conversation memory support
- Docker containerization
- Deployment to cloud (Render / Railway / VPS)
- Evaluation metrics for retrieval quality (MRR, NDCG)

---

## 👨‍💻 Author

Mohamed El-Nashar
