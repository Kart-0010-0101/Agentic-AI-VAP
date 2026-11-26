"""Automated tests for static audit, rubric penalties, full grading, and single-day ZIP export."""

from __future__ import annotations

import subprocess
import zipfile
from pathlib import Path

from evaluator.batch_grade import batch_grade_directory, evaluate_submission
from evaluator.release_day import export_day_zip
from evaluator.static_audit import audit_repository

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_day5_reference_scores_above_85(tmp_path: Path):
    day5_zip = export_day_zip(REPO_ROOT, "day-5", tmp_path / "day5.zip")
    sub_dir = tmp_path / "student_day5"
    with zipfile.ZipFile(day5_zip) as zf:
        zf.extractall(sub_dir)

    result = evaluate_submission(sub_dir, student_name="ref_day5", out_dir=tmp_path / "reports")
    assert result["score"]["total_score"] >= 85
    assert result["score"]["breakdown"]["react_loop_20"] == 20
    assert (tmp_path / "reports" / "ref_day5_evaluation.md").is_file()


def test_hardcoded_linear_script_gets_zero_for_react_loop(tmp_path: Path):
    bad_repo = tmp_path / "hardcoded_student"
    bad_repo.mkdir()
    (bad_repo / "README.md").write_text("# Student\n", encoding="utf-8")
    (bad_repo / "pyproject.toml").write_text('[project]\nname="x"\nversion="0.1"\n', encoding="utf-8")
    (bad_repo / "agent.py").write_text(
        "def run_agent(*a, **kw):\n"
        "    print('Step 1')\n"
        "    print('Step 2')\n"
        "    return {'steps': 2}\n",
        encoding="utf-8",
    )
    res = evaluate_submission(bad_repo, student_name="linear_student")
    assert res["static"]["has_react_loop"] is False
    assert res["score"]["breakdown"]["react_loop_20"] == 0


def test_leaked_api_secret_and_env_flagged(tmp_path: Path):
    leak_repo = tmp_path / "leaky"
    leak_repo.mkdir()
    (leak_repo / ".env").write_text("GROQ_API_KEY=gsk_1234567890abcdef\n", encoding="utf-8")
    (leak_repo / "agent.py").write_text('KEY = "gsk_1234567890abcdef1234"\n', encoding="utf-8")
    audit = audit_repository(leak_repo)
    assert audit["leaked_env"] is True
    assert "agent.py" in audit["secret_hits"]
    assert audit["secret_hygiene_ok"] is False


def test_release_day_exports_only_requested_branch_and_batch_leaderboard(tmp_path: Path):
    day1_zip = export_day_zip(REPO_ROOT, "day-1", tmp_path / "day1.zip")
    with zipfile.ZipFile(day1_zip) as zf:
        names = set(zf.namelist())
    assert "verify.py" in names
    assert "capstone_1_iot/agent.py" not in names

    # Quick batch leaderboard smoke check
    sub_root = tmp_path / "cohort"
    s1 = sub_root / "alice"
    s1.mkdir(parents=True)
    with zipfile.ZipFile(export_day_zip(REPO_ROOT, "day-5", tmp_path / "d5.zip")) as zf:
        zf.extractall(s1)
    csv_out = batch_grade_directory(sub_root, tmp_path / "leaderboard.csv")
    csv_text = csv_out.read_text(encoding="utf-8")
    assert "alice" in csv_text and "A+" in csv_text
