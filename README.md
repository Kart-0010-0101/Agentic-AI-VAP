# Day 3 — Closed-Loop ReAct Agent, Safe Tools, and Memory

Welcome to Day 3 of **AGENTIC AI VAP**. This branch builds a closed-loop ReAct agent with safe Python tools and cross-session ChromaDB memory.

## Files in This Branch
- `tools.py` — Sandboxed Python tools (`list_dir`, `read_file`, `search_kb`, `write_report`) that return error hints on missing files
- `memory.py` — ChromaDB store for short After-Action Review lessons (`store_aar`, `recall`)
- `aar_engine.py` — Helper that writes a one-sentence lesson from each step log
- `agent.py` — Bounded ReAct loop (`trace.jsonl`, `max_steps`, `--mock-llm`)
- `demo_cross_session.py` — Runs the task twice to show faster Run 2 execution from Run 1 memory
- `test_agent.py` — Tests self-healing recovery, step speedup, and loop caps

## Run Commands
```powershell
uv sync
uv run python demo_cross_session.py --mock-llm
uv run pytest test_agent.py -v
```
