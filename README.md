# Submission Grader and Single-Day Release Tool

Standalone instructor grader for **AGENTIC AI VAP**.

## Features
- **Code and Security Check (`static_audit.py`)**: Uses Python AST checks to mark hardcoded scripts `0/20` on ReAct Loop. Flags `.env` files and leaked `gsk_` or `sk-` keys.
- **Project 1 RAG Grader (`project1_grader.py`)**: Checks chunk overlap, idempotent `upsert()`, and MOSFET query match.
- **Agent and Fault Grader (`project2_grader.py` and `fault_injector.py`)**: Checks `trace.jsonl` format, missing-file recovery, NaN quarantine, and memory speedup.
- **Cohort Batch Grader (`batch_grade.py`)**: Grades a folder of student repos and saves a ranked CSV leaderboard.
- **Single-Day Export (`release_day.py`)**: Runs `git archive` on one day branch (`day-1` .. `day-5`) so students download only that day's files.

## CLI Commands
```powershell
uv sync
uv run python -m evaluator.cli evaluate <student_repo_path> --out reports/
uv run python -m evaluator.cli batch <submissions_root_dir> --out reports/leaderboard.csv
uv run python -m evaluator.cli release-day --repo . --branch day-1 --out releases/day-1.zip
uv run pytest tests/test_evaluator.py -v
```
