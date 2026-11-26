# Capstone 2 — 5G NR gNodeB Radio Triage Agent

Checks 5G FR1 cell KPIs against PRB, SINR, and BLER thresholds, moves broken rows to quarantine, and recalls AAR rules across runs.

```powershell
uv run python capstone_2_5g/ingest.py
uv run python capstone_2_5g/agent.py --mock-llm
uv run pytest capstone_2_5g/test_tools.py -v
```
