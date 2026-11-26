"""Check Python AST loops, missing docs, and leaked API secrets."""

from __future__ import annotations

import ast
import re
from pathlib import Path

SECRET_RE = re.compile(r"(gsk_[A-Za-z0-9]{12,}|sk-[A-Za-z0-9]{16,})")


def _has_control_loop(py_file: Path) -> bool:
    """Return True if an agent script contains an iterative While or bounded For step loop."""
    try:
        tree = ast.parse(py_file.read_text(encoding="utf-8", errors="ignore"))
    except SyntaxError:
        return False
    for node in ast.walk(tree):
        if isinstance(node, (ast.While, ast.For)):
            if any(isinstance(sub, ast.Call) for sub in ast.walk(node)):
                return True
    return False


def audit_repository(repo_dir: Path) -> dict:
    """Audit secrets, .env leaks, required files, and agent loop authenticity."""
    leaked_env = (repo_dir / ".env").exists()
    secret_hits: list[str] = []
    agent_files: list[Path] = []

    for path in sorted(repo_dir.rglob("*.py")):
        if ".venv" in path.parts or "__pycache__" in path.parts:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if SECRET_RE.search(text):
            secret_hits.append(str(path.relative_to(repo_dir)))
        if path.name == "agent.py":
            agent_files.append(path)

    has_readme = (repo_dir / "README.md").is_file()
    has_pyproject = (repo_dir / "pyproject.toml").is_file()
    loop_verified = any(_has_control_loop(p) for p in agent_files) if agent_files else False

    return {
        "leaked_env": leaked_env,
        "secret_hits": secret_hits,
        "secret_hygiene_ok": (not leaked_env) and (len(secret_hits) == 0),
        "has_readme": has_readme,
        "has_pyproject": has_pyproject,
        "agent_files": [str(p.relative_to(repo_dir)) for p in agent_files],
        "has_react_loop": loop_verified,
    }
