# Capstone 3 — ECE Literature Benchmark Agent

Checks research abstracts against edge latency and F1 score targets, isolates bad rows, and recalls AAR rules across runs.

```powershell
uv run python capstone_3_research/ingest.py
uv run python capstone_3_research/agent.py --mock-llm
uv run pytest capstone_3_research/test_tools.py -v
```
