# Capstone 2 — Autonomous 5G NR gNodeB Radio Triage Agent

Analyzes 5G FR1 cell KPIs against PRB, SINR, and BLER SLA limits with fault isolation and cross-session AAR memory.

```powershell
uv run python capstone_2_5g/ingest.py
uv run python capstone_2_5g/agent.py --mock-llm
uv run pytest capstone_2_5g/test_tools.py -v
```
