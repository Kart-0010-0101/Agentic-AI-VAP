# Day 1 — Toolchain Setup and Vector Search Lab

Welcome to Day 1 of the **5-Day Value Added Program** (Department of ECE, Acharya Institute of Technology).

## Files in This Branch
- `pyproject.toml` and `uv.lock` — Pinned Python 3.13 packages (`chromadb`, `duckduckgo-search`, `pydantic`, `python-dotenv`, `requests`, `pytest`)
- `.env.example` — Sample file for your `GROQ_API_KEY`. Never commit `.env`.
- `verify.py` — Script that checks Groq HTTPS access and ChromaDB install.
- `chroma_demo.py` — Vector search lab with 384-D local ONNX embeddings.

## Run Locally
```powershell
uv sync
Copy-Item .env.example .env
# Put your GROQ_API_KEY in .env
uv run python verify.py
uv run python chroma_demo.py
```
