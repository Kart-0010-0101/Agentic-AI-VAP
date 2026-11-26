"""Check that the repository contains zero .env files or hardcoded API keys."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SECRET_PATTERN = re.compile(r"(gsk_[A-Za-z0-9]{12,}|sk-[A-Za-z0-9]{16,})")


def test_no_committed_env_or_api_secrets():
    assert (ROOT / "pyproject.toml").is_file()
    assert (ROOT / "README.md").is_file()
    assert not (ROOT / ".env").exists(), ".env file must never exist inside clean repo!"

    for path in ROOT.rglob("*.py"):
        if ".venv" in path.parts:
            continue
        content = path.read_text(encoding="utf-8", errors="ignore")
        assert not SECRET_PATTERN.search(content), f"Possible API secret found in {path}"
