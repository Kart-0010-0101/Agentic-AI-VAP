# Automated VAP Submission Evaluator & Per-Day Release Tool

Standalone instructor evaluation harness for **AGENTIC AI VAP**.

## Capabilities
- **Static & Security Audit (`static_audit.py`)**: AST check flagging hardcoded linear scripts (`0/20` on ReAct Loop), `.env` leak check, hardcoded `gsk_`/`sk-` secret scanner, required files check.
- **Project 1 RAG Grader (`project1_grader.py`)**: Verifies chunking overlap, idempotent `upsert()`, and retrieval precision.
- **Project 2 & Capstone Grader (`project2_grader.py` + `fault_injector.py`)**: Verifies `trace.jsonl` schema, multi-step fault recovery on unseen corrupt inputs, and cross-session episodic speedup.
- **Batch Leaderboard (`batch_grade.py`)**: Evaluates a folder of student submissions into a ranked CSV leaderboard + individual Markdown/JSON reports.
- **Per-Day Student Release (`release_day.py`)**: Exports a single day branch (`day-1` .. `day-5`) via `git archive` as a clean ZIP so students only receive that day's files.

## CLI Usage
```powershell
uv sync
uv run python -m evaluator.cli evaluate <student_repo_path> --out reports/
uv run python -m evaluator.cli batch <submissions_root_dir> --out reports/leaderboard.csv
uv run python -m evaluator.cli release-day --repo . --branch day-1 --out releases/day-1.zip
uv run pytest tests/test_evaluator.py -v
```
