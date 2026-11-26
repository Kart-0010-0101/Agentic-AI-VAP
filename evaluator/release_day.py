"""Export a single day's Git branch via `git archive` so students download ONLY that day's files."""

from __future__ import annotations

import subprocess
from pathlib import Path


def export_day_zip(repo_dir: Path, branch: str, out_zip: Path) -> Path:
    """Create a clean student ZIP archive containing strictly the tree of `branch`."""
    out_zip.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["git", "-C", str(repo_dir), "archive", "--format=zip", "--output", str(out_zip), branch]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"git archive failed for branch '{branch}': {res.stderr.strip()}")
    return out_zip
