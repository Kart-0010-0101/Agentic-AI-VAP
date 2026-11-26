"""Generate crisp Markdown and JSON student evaluation reports."""

from __future__ import annotations

import json
from pathlib import Path


def write_evaluation_reports(student_name: str, payload: dict, out_dir: Path) -> tuple[Path, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / f"{student_name}_evaluation.json"
    md_path = out_dir / f"{student_name}_evaluation.md"

    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    score = payload["score"]
    b = score["breakdown"]
    deductions = "\n".join(f"- {d}" for d in score["deductions"]) or "- None (Full Pass)"
    md = (
        f"# Evaluation Report — {student_name}\n\n"
        f"- **Final Score**: **{score['total_score']} / {score['max_score']}** (Grade: **{score['grade']}**)\n"
        f"- **AST ReAct Loop Verified**: `{payload['static']['has_react_loop']}`\n"
        f"- **Secret Hygiene Clean**: `{payload['static']['secret_hygiene_ok']}`\n\n"
        "## Score Breakdown\n"
        f"- RAG Pipeline (25): **{b['rag_pipeline_25']} / 25**\n"
        f"- ReAct Loop & Trace (20): **{b['react_loop_20']} / 20**\n"
        f"- Fault Recovery & Quarantine (25): **{b['fault_recovery_25']} / 25**\n"
        f"- Episodic Memory Speedup (20): **{b['episodic_memory_20']} / 20**\n"
        f"- Hygiene & Docs (10): **{b['hygiene_and_docs_10']} / 10**\n\n"
        f"## Deductions & Diagnostics\n{deductions}\n"
    )
    md_path.write_text(md, encoding="utf-8")
    return md_path, json_path
