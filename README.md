# AGENTIC AI VAP

**Engineering Autonomous Agentic AI Systems with Vector RAG Memory**  
5-Day Value Added Program (VAP) — Department of ECE, Acharya Institute of Technology

## Repository Branch Architecture

Each workshop day and the automated grading suite live on dedicated branches so materials stay modular and can be exported individually per session:

| Branch | Contents |
| :--- | :--- |
| `main` | Repository documentation (`README.md`) and Apache 2.0 `LICENSE` only |
| `day-1` | Environment verification (`verify.py`), ChromaDB semantic search lab (`chroma_demo.py`), and anonymous classroom mobile poll server (`live_poll/`) |
| `day-2` | Project 1: Complete Vector RAG system (`knowledge_base/`, `ingest.py`, `query.py`, `test_rag.py`) |
| `day-3` | Autonomous ReAct while-loop (`agent.py`), `@register_tool` tool calling (`tools.py`), persistent ChromaDB episodic memory (`memory.py`), After Action Review (`aar_engine.py`), and capstone dataset generator |
| `day-4` | All 3 complete Capstone Projects (`capstone_1_iot/`, `capstone_2_5g/`, `capstone_3_research/`), each with domain ingestion, 4 typed defensive tools, autonomous loop, `trace.jsonl`, and standalone unit tests |
| `day-5` | Hardened capstones + verification & fault-injection test suite (`testing/`) and unseen evaluator benchmark datasets |
| `auto-evaluator` | Standalone automated submission checker, tester, grader & evaluator (`evaluator/`) for student repositories and batch class grading, plus daily archive exporter (`release_day.py`) |

## Daily Schedule (`09:30 - 17:00`)

- **Session 1 (Morning Theory)**: `09:30 - 11:00`
- **Morning Break**: `11:00 - 11:30`
- **Session 2 (Morning Theory)**: `11:30 - 13:00`
- **Lunch Break**: `13:00 - 14:00`
- **Session 3 (Afternoon Working Lab)**: `14:00 - 17:00`

## License

Licensed under the [Apache License, Version 2.0](LICENSE).
