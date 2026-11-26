# Capstone 1 — IoT Fleet Fault Agent

Checks edge JSON logs against IRF540N MOSFET and enclosure heat limits, moves NaN rows to quarantine, fixes missing file paths, and stores AAR rules in ChromaDB.

```powershell
uv run python capstone_1_iot/ingest.py
uv run python capstone_1_iot/agent.py --mock-llm
uv run pytest capstone_1_iot/test_tools.py -v
```
