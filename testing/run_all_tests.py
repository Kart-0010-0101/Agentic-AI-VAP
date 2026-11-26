"""Day 5 single-command verification runner across all unit, capstone & fault suites."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SUITES = [
    ("Day 2 Vector RAG", "test_rag.py"),
    ("Day 3 ReAct + Memory", "test_agent.py"),
    ("Capstone 1: IoT Fleet", "capstone_1_iot/test_tools.py"),
    ("Capstone 2: 5G NR", "capstone_2_5g/test_tools.py"),
    ("Capstone 3: Research", "capstone_3_research/test_tools.py"),
    ("Day 5 Fault Injection", "testing/test_fault_injection.py"),
    ("Day 5 Cross-Session", "testing/test_cross_session_memory.py"),
    ("Day 5 Trace Contract", "testing/test_trace_contract.py"),
    ("Day 5 Repo Hygiene", "testing/test_repo_hygiene.py"),
]


def main() -> int:
    print("=" * 64)
    print("VAP DAY 5 MASTER VERIFICATION HARNESS")
    print("=" * 64)
    failures = 0
    for label, target in SUITES:
        res = subprocess.run([sys.executable, "-m", "pytest", target, "-q"], cwd=ROOT)
        status = "PASS" if res.returncode == 0 else "FAIL"
        if res.returncode != 0:
            failures += 1
        print(f"[{status}] {label:<28} ({target})")
    print("=" * 64)
    print(f"Summary: {len(SUITES) - failures}/{len(SUITES)} suites passed.")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
