# Capstone 1 — Autonomous IoT Sensor Fleet Fault Diagnosis

Inspects edge telemetry JSON against IRF540N MOSFET and thermal enclosure limits, quarantines corrupt/NaN records without crashing, self-heals missing paths, and stores After-Action Review rules in ChromaDB.

```powershell
uv run python capstone_1_iot/ingest.py
uv run python capstone_1_iot/agent.py --mock-llm
uv run pytest capstone_1_iot/test_tools.py -v
```
