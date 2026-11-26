"""Load student submission from a local path or Git repository URL into an isolated sandbox."""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path


def load_submission(source: str | Path) -> tuple[Path, bool]:
    """Return (workspace_path, is_temp). Clones git URLs or copies local dirs into temp sandbox."""
    src_str = str(source)
    tmp_dir = Path(tempfile.mkdtemp(prefix="vap_eval_"))
    if src_str.startswith(("http://", "https://", "git@")):
        res = subprocess.run(["git", "clone", "--depth", "1", src_str, str(tmp_dir)], capture_output=True, text=True)
        if res.returncode != 0:
            shutil.rmtree(tmp_dir, ignore_errors=True)
            raise RuntimeError(f"Git clone failed for {src_str}: {res.stderr.strip()}")
        return tmp_dir, True

    src_path = Path(source).resolve()
    if not src_path.is_dir():
        shutil.rmtree(tmp_dir, ignore_errors=True)
        raise FileNotFoundError(f"Submission directory not found: {src_path}")

    def _ignore(_dir: str, names: list[str]) -> set[str]:
        return {n for n in names if n in {".git", ".venv", "__pycache__", ".pytest_cache", "chroma_db", "agent_memory", "capstone_memory"}}

    shutil.copytree(src_path, tmp_dir, dirs_exist_ok=True, ignore=_ignore)
    return tmp_dir, True
