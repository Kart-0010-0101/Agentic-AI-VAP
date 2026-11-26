"""Day 1 preflight verification for Groq API HTTPS connectivity and ChromaDB."""

from __future__ import annotations

import json
import os
import sys
import urllib.request
import chromadb
from dotenv import load_dotenv


def verify_environment() -> bool:
    load_dotenv()
    api_key = os.environ.get("GROQ_API_KEY", "").strip()
    if not api_key or api_key == "gsk_replace_with_your_real_key":
        print("ChromaDB Version:", chromadb.__version__)
        print("GROQ_API_KEY missing or placeholder in .env — skipping live network call.")
        return False

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    body = json.dumps({
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": "Say hello in 1 word."}],
        "max_tokens": 10,
    }).encode("utf-8")
    req = urllib.request.Request(
        "https://api.groq.com/openai/v1/chat/completions",
        data=body,
        headers=headers,
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        res = json.loads(resp.read().decode("utf-8"))
    print("API Connected:", res["choices"][0]["message"]["content"])
    print("ChromaDB Version:", chromadb.__version__)
    return True


if __name__ == "__main__":
    ok = verify_environment()
    sys.exit(0 if ok else 1)
