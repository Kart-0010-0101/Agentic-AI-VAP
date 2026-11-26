# Day 2 — Project 1: End-to-End ECE Vector RAG Pipeline

Welcome to Day 2 of **AGENTIC AI VAP**. Today builds a production-clean, idempotent **Vector RAG** pipeline over real ECE datasheets.

## Contents
- `knowledge_base/` — 4 technical ECE documents (`irf540n_mosfet.md`, `esp32_s3_datasheet.md`, `5g_nr_prb_spec.md`, `lorawan_bms_notes.md`)
- `ingest.py` — Overlapping chunker (`chunk_size=500, overlap=50`) + idempotent `collection.upsert()`
- `query.py` — Top-k semantic retrieval with distance gating + Groq HTTPS synthesis (`--mock-llm` supported for offline CI)
- `test_rag.py` — Automated pytest suite verifying overlap, idempotent re-ingestion, and citation accuracy

## Quick Start
```powershell
uv sync
uv run python ingest.py
uv run python query.py "What is the max Vds of IRF540N?" --mock-llm
uv run pytest test_rag.py -v
```
