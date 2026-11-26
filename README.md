# Day 5 — Fault Injection, Unseen Tests, and Live Defense

Welcome to Day 5 of **AGENTIC AI VAP**. This branch adds toxic JSON fault handling across all three capstones and provides the `testing/` suite.

## Test Files (`testing/`)
- `testing/unseen_benchmarks/` — Unseen Batch B files (`iot_batch_b.json`, `gnb_batch_b.json`, `papers_batch_b.json`, `corrupt_malformed.json`)
- `testing/test_fault_injection.py` — Checks NaN and corrupt JSON quarantine with zero tracebacks
- `testing/test_cross_session_memory.py` — Checks faster Run 2 steps from ChromaDB memory
- `testing/test_trace_contract.py` — Checks the 7 fixed JSON keys in `trace.jsonl`
- `testing/test_repo_hygiene.py` — Checks for leaked `.env` files or API keys
- `testing/run_all_tests.py` — Runs all 9 test suites and prints the summary table

## Run All Checks
```powershell
uv sync
uv run python testing/run_all_tests.py
```
