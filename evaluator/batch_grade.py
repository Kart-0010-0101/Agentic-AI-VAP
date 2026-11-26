"""Grade one submission or a full student cohort folder into CSV."""

from __future__ import annotations

import csv
import shutil
from pathlib import Path

from evaluator.fault_injector import run_fault_injection
from evaluator.project1_grader import grade_project1
from evaluator.project2_grader import grade_project2
from evaluator.repo_loader import load_submission
from evaluator.report_generator import write_evaluation_reports
from evaluator.rubric import compute_score
from evaluator.static_audit import audit_repository


def evaluate_submission(source: str | Path, student_name: str | None = None, out_dir: Path | None = None) -> dict:
    workspace, is_temp = load_submission(source)
    name = student_name or Path(str(source).rstrip("/\\")).name
    try:
        static_res = audit_repository(workspace)
        rag_res = grade_project1(workspace)
        agent_res = grade_project2(workspace)
        fault_res = run_fault_injection(workspace)
        score = compute_score(static_res, rag_res, agent_res, fault_res)
        payload = {
            "student": name,
            "score": score,
            "static": static_res,
            "rag": rag_res,
            "agent": agent_res,
            "fault": fault_res,
        }
        if out_dir is not None:
            write_evaluation_reports(name, payload, out_dir)
        return payload
    finally:
        if is_temp:
            shutil.rmtree(workspace, ignore_errors=True)


def batch_grade_directory(submissions_root: Path, out_csv: Path, reports_dir: Path | None = None) -> Path:
    results = []
    for sub in sorted(submissions_root.iterdir()):
        if sub.is_dir() and not sub.name.startswith("."):
            results.append(evaluate_submission(sub, student_name=sub.name, out_dir=reports_dir or out_csv.parent))

    results.sort(key=lambda r: r["score"]["total_score"], reverse=True)
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["rank", "student", "total_score", "grade", "react_loop", "secret_clean", "top_deduction"])
        for rank, r in enumerate(results, start=1):
            sc = r["score"]
            writer.writerow([
                rank,
                r["student"],
                sc["total_score"],
                sc["grade"],
                r["static"]["has_react_loop"],
                r["static"]["secret_hygiene_ok"],
                sc["deductions"][0] if sc["deductions"] else "None",
            ])
    return out_csv
