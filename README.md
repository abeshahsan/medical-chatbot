<h1 align="center">Medical Knowledge RAG Assistant</h1>

<p align="center">
	<img src="https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white" alt="Python 3.10" />
	<img src="https://img.shields.io/badge/Flask-3.1.1-000000?logo=flask&logoColor=white" alt="Flask" />
	<img src="https://img.shields.io/badge/LangChain-0.3.x-1C3C3C?logo=langchain&logoColor=white" alt="LangChain" />
	<img src="https://img.shields.io/badge/Pinecone-Vector_DB-005BD4?logo=pinecone&logoColor=white" alt="Pinecone" />
</p>
<p align="center">
	<img src="https://img.shields.io/badge/OpenRouter-GPT--4o-6D4AFF?logo=openai&logoColor=white" alt="OpenRouter GPT-4o" />
	<img src="https://img.shields.io/badge/HuggingFace-BAAI%2Fbge--small--en--v1.5-FF9D00?logo=huggingface&logoColor=black" alt="BGE Small Embeddings" />
	<img src="https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker&logoColor=white" alt="Docker" />
</p>

---

# Overview

This project implements a medical-domain Retrieval-Augmented Generation (RAG) assistant that answers user questions through a Flask web app and a retrieval chain built with LangChain.
It combines a local embedding model (`BAAI/bge-small-en-v1.5`) with Pinecone vector search and a GPT-4o chat model accessed through OpenRouter's OpenAI-compatible endpoint.
The app retrieves top-k context chunks from an existing Pinecone index, injects them into a constrained medical assistant prompt, and returns concise responses.
The frontend supports conversational UX and sends recent dialogue history to improve response continuity.
The repository also includes local Docker-based build/run automation via a batch pipeline for reproducible deployment steps.

---

# Features

- PDF ingestion utilities are implemented via `PyPDFDirectoryLoader` in `src/doc_helper.py` (recursive directory load).
- Minimal ingestion entrypoint is available via `ingest.py` to load PDFs from `data/`, chunk, and upsert into Pinecone.
- Text chunking is implemented with `RecursiveCharacterTextSplitter` using `chunk_size=500` and `chunk_overlap=200`.
- Embedding model: Hugging Face `BAAI/bge-small-en-v1.5` via `HuggingFaceEmbeddings`.
- Embedding runtime automatically selects `cuda` when available, otherwise CPU.
- Vector database: Pinecone serverless index (`metric=cosine`, `dimension=384`, AWS `us-east-1`).
- Retrieval strategy: similarity search with `k=3` (`as_retriever(search_type="similarity")`).
- LLM integration: `ChatOpenAI` client targeting OpenRouter (`model="gpt-4o"`, `max_completion_tokens=512`).
- Web interface and API: Flask app with `/` (UI) and `/chat` (POST JSON) endpoints.
- Containerized serving: Gunicorn in Docker, exposed on port `5000`.
- Local CI/CD-style pipeline: `pipeline.bat` installs dependencies, runs test stage placeholder, builds Docker image, and runs container.

---

# Architecture & RAG Pipeline

1. Data Ingestion
	 - `load_pdf_files(path)` in `src/doc_helper.py` loads PDF files from a directory recursively.
2. Preprocessing & Chunking
	 - `filter_minimal_docs(...)` keeps only minimal metadata (`source`).
	 - `split_and_chunk(...)` creates overlapping chunks for retrieval quality.
3. Embedding & Indexing
	 - `get_embeddings(...)` in `src/embedding_model.py` generates embeddings with BGE-small.
	 - `get_vector_db()` in `src/vector_db.py` can create the Pinecone index if missing.
	 - Runtime retrieval uses `PineconeVectorStore.from_existing_index(...)`.
4. Retrieval
	 - `get_retriever(..., k=3)` returns a similarity retriever.
5. Generation
	 - `get_prompt()` defines a medical assistant system prompt.
	 - `get_rag_chain(...)` composes retrieval + document stuffing chain.
	 - Flask `/chat` endpoint invokes `rag_chain.invoke({"input": ...})` and returns answer JSON.

```text
User (Web UI)
	 |
	 v
POST /chat --------------> Flask app (app.py)
                                    |
                                    v
                        LangChain Retrieval Chain
                        |                      |
                        v                      v
            Pinecone Retriever      ChatOpenAI (gpt-4o via OpenRouter)
                        |                      ^
                        v                      |
        Retrieved context chunks ------+
                                    |
                                    v
                        Final answer JSON
```

---

# CI/CD Pipeline (Local with Docker)

The project includes a local pipeline script: `pipeline.bat`.

Pipeline stages currently implemented:

1. Install runtime dependencies (`requirements.txt`).
2. Install development dependencies (`requirements-dev.txt`).
3. Run a test stage placeholder (currently prints `No tests yet`).
4. Build Docker image: `docker build -t rag-backend .`.
5. Run container: `docker run -d -p 5000:5000 --name rag-app rag-backend`.

Docker runtime details:

- Base image: `python:3.10-slim`.
- Installs `gunicorn==22.0.0`.
- Installs CPU PyTorch wheel explicitly.
- Exposes `5000` and serves Flask app through Gunicorn.

This gives a repeatable local delivery flow that simulates CI/CD steps without external CI infrastructure.

---

# Installation

1. Clone the repository

```bash
git clone <your-repo-url>
cd medical-chat-rag
```

2. Set up Python environment (local)

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
pip install -e .
```

4. Configure environment variables

```bash
copy .env.example .env   # Windows
# cp .env.example .env   # Linux/macOS
```

Set values in `.env`:

```env
PINECONE_API_KEY=...
OPENROUTER_API_KEY=...
OPENROUTER_BASE_URL=...
```

5. Build and run with Docker (optional)

```bash
docker build -t rag-backend .
docker run -d -p 5000:5000 --name rag-app rag-backend
```

---

# Usage

Run locally:

```bash
python app.py
```

Open browser:

- `http://localhost:5000`

API endpoint:

- `POST /chat`
- Request body:

```json
{
	"message": "What are common causes of acne?",
	"history": [
		{"role": "user", "text": "I have recurring breakouts."},
		{"role": "bot", "text": "Can you describe where and when they occur?"}
	]
}
```

- Response body:

```json
{
	"msg": "...generated answer..."
}
```

Example questions:

- `What do you know about acne?`
- `What symptoms are associated with iron deficiency?`

How to add new documents:

- Place PDFs in `data/` (the repo currently includes `data/Medical_book.pdf`).
- Run ingestion to (re)index the current PDFs into Pinecone:

```bash
python ingest.py
```

- Ingestion uses existing helpers in `src/doc_helper.py` and writes chunks to the `medical-chatbot` index.

---

# Tech Stack

<p>
	<img src="https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white" alt="Python 3.10" />
	<img src="https://img.shields.io/badge/Flask-3.1.1-000000?logo=flask&logoColor=white" alt="Flask" />
	<img src="https://img.shields.io/badge/LangChain-core%20%7C%20community%20%7C%20openai%20%7C%20pinecone-1C3C3C?logo=langchain&logoColor=white" alt="LangChain ecosystem" />
	<img src="https://img.shields.io/badge/OpenRouter-GPT--4o-6D4AFF?logo=openai&logoColor=white" alt="OpenRouter GPT-4o" />
	<img src="https://img.shields.io/badge/Pinecone-Serverless-005BD4?logo=pinecone&logoColor=white" alt="Pinecone" />
	<img src="https://img.shields.io/badge/SentenceTransformers-BAAI%2Fbge--small--en--v1.5-FF9D00?logo=huggingface&logoColor=black" alt="Sentence Transformers" />
	<img src="https://img.shields.io/badge/PyPDF-PDF_Processing-CC0000" alt="PyPDF" />
	<img src="https://img.shields.io/badge/Gunicorn-22.0.0-499848" alt="Gunicorn" />
	<img src="https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker&logoColor=white" alt="Docker" />
	<img src="https://img.shields.io/badge/Pytest-Testing-0A9EDC?logo=pytest&logoColor=white" alt="Pytest" />
</p>

---

# Configuration

Key configurable parameters in code:

- Chunk size and overlap:
	- `src/doc_helper.py`: `RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=200)`
- Embedding model:
	- `src/constants.py`: `EMBEDDING_MODEL_NAME = "BAAI/bge-small-en-v1.5"`
- Retrieval parameters:
	- `app.py` and `main.py`: `get_retriever(..., k=3)`
- LLM/provider settings:
	- `src/llm.py`: `model="gpt-4o"`, `max_completion_tokens=512`
	- `.env`: `OPENROUTER_API_KEY`, `OPENROUTER_BASE_URL`
- Vector index settings:
	- `src/vector_db.py`: index name `medical-chatbot`, cosine metric, dimension `384`

---

# Requirements

- Python: 3.10.x (Dockerfile uses `python:3.10-slim`)
- OS: Windows/Linux/macOS (Windows batch pipeline included)
- Compute: CPU-friendly by default; embeddings switch to GPU automatically if CUDA is available
- Docker: required for containerized run and local pipeline Docker stages
- External services: Pinecone account/API key and OpenRouter API key

---

# Project Structure

```text
medical-chat-rag/
├─ app.py                      # Flask app, routes, and RAG invocation
├─ ingest.py                   # Minimal PDF -> chunk -> Pinecone ingestion script
├─ main.py                     # Simple direct RAG invocation script
├─ pipeline.bat                # Local CI/CD-style automation (install/build/run)
├─ Dockerfile                  # Container build and Gunicorn startup
├─ requirements.txt            # Runtime dependencies
├─ requirements-dev.txt        # Dev/test dependencies
├─ setup.py                    # Package metadata
├─ data/
│  └─ Medical_book.pdf         # Source knowledge document(s)
├─ frontend/
│  ├─ index.html               # Chat UI template
│  └─ static/
│     ├─ index.css             # UI styles
│     └─ index.js              # Client-side chat logic
├─ src/
│  ├─ constants.py             # Env vars and global config constants
│  ├─ doc_helper.py            # PDF loading and chunking utilities
│  ├─ embedding_model.py       # Embedding model construction
│  ├─ vector_db.py             # Pinecone index/vector store/retriever helpers
│  ├─ llm.py                   # LLM client configuration (OpenRouter)
│  ├─ prompt.py                # Prompt template definition
│  └─ rag_chain.py             # Retrieval + generation chain assembly
└─ tests/
	 └─ test_api.py              # Test placeholder (currently empty)
```

---

# Contributing

1. Create a feature branch.
2. Keep changes focused and include tests when adding behavior.
3. Ensure local run works (`python app.py`) and Docker build succeeds.
4. Open a pull request with a concise technical summary.

---

