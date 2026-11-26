# Day 4 — All 3 Unassisted Capstone Tracks (IoT, 5G NR, Research)

Welcome to Day 4 of **AGENTIC AI VAP**. All three capstone problem statements live here as complete, standalone closed-loop systems:

- `capstone_1_iot/` — IoT Sensor Fleet Fault Diagnosis (`read_telemetry`, `query_specs`, `list_dir`, `write_report`)
- `capstone_2_5g/` — 5G NR gNodeB Radio Triage (`read_kpis`, `query_sla`, `list_dir`, `write_report`)
- `capstone_3_research/` — Autonomous Research Benchmark Synthesizer (`read_papers`, `query_standards`, `list_dir`, `write_report`)

## Quick Verification Across All 3 Capstones
```powershell
uv sync
uv run pytest capstone_1_iot/test_tools.py capstone_2_5g/test_tools.py capstone_3_research/test_tools.py -v
```
