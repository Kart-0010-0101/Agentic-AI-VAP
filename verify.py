"""Check Groq API HTTPS access and local ChromaDB setup."""

from __future__ import annotations

import os
import sys
import chromadb
import requests
from dotenv import load_dotenv

DEFAULT_GROQ_MODEL = "qwen/qwen3.8-27b"


def verify_environment() -> bool:
    load_dotenv()
    api_key = os.environ.get("GROQ_API_KEY", "").strip()
    if not api_key or api_key == "gsk_replace_with_your_real_key":
        print("ChromaDB Version:", chromadb.__version__)
        print("GROQ_API_KEY missing or placeholder in .env — skipping live network call.")
        return False

    model = os.environ.get("GROQ_MODEL", DEFAULT_GROQ_MODEL).strip() or DEFAULT_GROQ_MODEL
    resp = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": model,
            "messages": [{"role": "user", "content": "Say hello in 1 word."}],
            "max_tokens": 32,
        },
        timeout=20,
    )
    resp.raise_for_status()
    res = resp.json()
    print("API Connected:", res["choices"][0]["message"]["content"].strip())
    print("Model:", model)
    print("ChromaDB Version:", chromadb.__version__)
    return True


if __name__ == "__main__":
    ok = verify_environment()
    sys.exit(0 if ok else 1)
