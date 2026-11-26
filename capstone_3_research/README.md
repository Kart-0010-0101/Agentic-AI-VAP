# Capstone 3 — Autonomous ECE Research & Benchmark Synthesizer

Evaluates technical abstracts against latency and F1 production thresholds, isolates malformed entries, and recalls cross-session lessons.

```powershell
uv run python capstone_3_research/ingest.py
uv run python capstone_3_research/agent.py --mock-llm
uv run pytest capstone_3_research/test_tools.py -v
```
