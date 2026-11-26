# Day 2 — Project 1: ECE Vector RAG Pipeline

Welcome to Day 2 of **AGENTIC AI VAP**. This branch builds an idempotent Vector RAG tool over technical ECE datasheets.

## Files in This Branch
- `knowledge_base/` — Four ECE technical docs (`irf540n_mosfet.md`, `esp32_s3_datasheet.md`, `5g_nr_prb_spec.md`, `lorawan_bms_notes.md`)
- `ingest.py` — Chunk text with 50-char overlap and run `collection.upsert()` safely
- `query.py` — Find top-k chunks within distance limits and generate cited Groq replies (`--mock-llm` runs offline)
- `test_rag.py` — Automated pytest suite for overlap, idempotency, and citations

## Run Commands
```powershell
uv sync
uv run python ingest.py
uv run python query.py "What is the max Vds of IRF540N?" --mock-llm
uv run pytest test_rag.py -v
```
