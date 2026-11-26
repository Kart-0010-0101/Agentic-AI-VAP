"""Unified CLI for VAP submission evaluation, batch CSV grading, and per-day student ZIP release."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from evaluator.batch_grade import batch_grade_directory, evaluate_submission
from evaluator.release_day import export_day_zip


def main() -> int:
    parser = argparse.ArgumentParser(description="AGENTIC AI VAP Automated Evaluator CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    p_eval = sub.add_parser("evaluate", help="Evaluate one student submission path or Git URL.")
    p_eval.add_argument("source", type=str)
    p_eval.add_argument("--name", type=str, default=None)
    p_eval.add_argument("--out", type=Path, default=Path("reports"))

    p_batch = sub.add_parser("batch", help="Batch-grade a directory of student folders into CSV leaderboard.")
    p_batch.add_argument("submissions_dir", type=Path)
    p_batch.add_argument("--out", type=Path, default=Path("reports/leaderboard.csv"))

    p_rel = sub.add_parser("release-day", help="Export strictly a single day branch as a clean student ZIP.")
    p_rel.add_argument("--repo", type=Path, default=Path("."))
    p_rel.add_argument("--branch", required=True)
    p_rel.add_argument("--out", type=Path, required=True)

    args = parser.parse_args()
    if args.command == "evaluate":
        res = evaluate_submission(args.source, student_name=args.name, out_dir=args.out)
        print(json.dumps(res["score"], indent=2))
        return 0
    if args.command == "batch":
        csv_path = batch_grade_directory(args.submissions_dir, args.out)
        print(f"Wrote leaderboard CSV to {csv_path}")
        return 0
    if args.command == "release-day":
        zip_path = export_day_zip(args.repo, args.branch, args.out)
        print(f"Exported clean single-day bundle to {zip_path}")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
