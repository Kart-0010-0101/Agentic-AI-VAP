"""Run the agent twice to show faster step count after cold memory recall."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path
from agent import run_agent


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mock-llm", action="store_true")
    args = parser.parse_args()

    base = Path(__file__).resolve().parent
    mem_dir = base / "agent_memory"
    shutil.rmtree(mem_dir, ignore_errors=True)
    goal = "Audit IoT node thermal anomalies and generate out/audit_report.md"

    run1 = run_agent(goal, workdir=base, db_dir=mem_dir, trace_path=base / "trace_run1.jsonl", mock_llm=args.mock_llm)
    print(f"Run 1 (Cold Start): {run1['steps']} steps | Recalled: {run1['recalled_precedents']} | AAR: {run1['aar_lesson']}")

    run2 = run_agent(goal, workdir=base, db_dir=mem_dir, trace_path=base / "trace_run2.jsonl", mock_llm=args.mock_llm)
    print(f"Run 2 (Warm Recall): {run2['steps']} steps | Recalled: {run2['recalled_precedents']} | AAR: {run2['aar_lesson']}")


if __name__ == "__main__":
    main()
