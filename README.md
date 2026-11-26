# Day 3 — Closed-Loop ReAct Agent, Self-Healing Tools & Episodic Memory

Welcome to Day 3 of **AGENTIC AI VAP**. Today transitions from static RAG pipelines to an autonomous `while`-loop ReAct agent with structured error recovery and cross-session After-Action Review (AAR) memory.

## Contents
- `tools.py` — Defensive tools (`list_dir`, `read_file`, `search_kb`, `write_report`) returning actionable JSON hints on failure
- `memory.py` — Persistent ChromaDB episodic memory (`store_aar`, `recall`)
- `aar_engine.py` — Distills concise 1-sentence lessons from traces without raw-log pollution
- `agent.py` — Closed-loop ReAct execution engine (`trace.jsonl`, `max_steps`, `--mock-llm`)
- `demo_cross_session.py` — Proves Run 2 solves the task in 50% fewer steps using Run 1's AAR
- `test_agent.py` — Verifies error recovery, trace contracts, speedup, and loop caps

## Quick Start
```powershell
uv sync
uv run python demo_cross_session.py --mock-llm
uv run pytest test_agent.py -v
```
