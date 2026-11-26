# Day 4 — Capstone Tracks: IoT, 5G NR, and Research

Welcome to Day 4 of **AGENTIC AI VAP**. This branch holds all three capstone systems:

- `capstone_1_iot/` — IoT Fleet fault agent (`read_telemetry`, `query_specs`, `list_dir`, `write_report`)
- `capstone_2_5g/` — 5G NR cell radio triage agent (`read_kpis`, `query_sla`, `list_dir`, `write_report`)
- `capstone_3_research/` — ECE paper benchmark agent (`read_papers`, `query_standards`, `list_dir`, `write_report`)

## Test All Three Capstones
```powershell
uv sync
uv run pytest capstone_1_iot/test_tools.py capstone_2_5g/test_tools.py capstone_3_research/test_tools.py -v
```
