# Day 5 — Verification, Fault Injection & Live Defense Suite

Welcome to Day 5 of **AGENTIC AI VAP**. This branch hardens all 3 capstones against unseen malformed telemetry and adds the full verification test harness under `testing/`.

## Testing Suite (`testing/`)
- `testing/unseen_benchmarks/` — Unseen Batch B datasets (`iot_batch_b.json`, `gnb_batch_b.json`, `papers_batch_b.json`, `corrupt_malformed.json`)
- `testing/test_fault_injection.py` — Validates graceful `NaN` / corrupt JSON quarantine without tracebacks
- `testing/test_cross_session_memory.py` — Verifies cross-session AAR speedup across all 3 capstones
- `testing/test_trace_contract.py` — Enforces strict `trace.jsonl` telemetry schema
- `testing/test_repo_hygiene.py` — Zero-trust secret & `.env` hygiene verification
- `testing/run_all_tests.py` — Master verification harness

## Run All Checks
```powershell
uv sync
uv run python testing/run_all_tests.py
```
