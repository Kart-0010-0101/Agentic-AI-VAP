# 5-Day Value Added Program (VAP): Engineering Autonomous Agentic AI Systems with Vector RAG Memory

- **Course Title**: Engineering Autonomous Agentic AI Systems with Vector RAG Memory
- **Institution**: Acharya Institute of Technology, Bengaluru
- **Department**: Department of Electronics and Communication Engineering (ECE)
- **Target Audience**: ECE 5th Semester, 3rd Year Undergraduate Students
- **Duration**: 5 Days (Full-time intensive workshop, 6-7 hours/day)
- **Pedagogy**: Conceptual clarity, mathematical foundations, instructor live demonstrations, hands-on guided builds, and independent capstone execution
- **Instructor Role**: Mentor and guide for Days 1 to 3; Evaluator only for Days 4 and 5
- **Reference Formats**: A4 Student Workshop Handbook & A4 Instructor Preparation Handbook

---

## 1. Executive Course Overview

This 5-day intensive Value Added Program bridges the gap between passive Large Language Model (LLM) applications and autonomous agentic software architectures. 

Electronics and communication engineering students move beyond prompt engineering and single-turn query wrappers. Students build production-grade autonomous agent loops from first principles in pure Python 3.13, integrating Vector Retrieval-Augmented Generation (RAG) not merely as a document search engine, but as long-term episodic and semantic memory for an autonomous agent.

Students will progress through two distinct engineering projects:

- **Project 1 (Guided Build — Days 1 & 2)**: A functional Vector RAG system that ingests domain technical documentation, generates dense vector representations, indexes them in ChromaDB using HNSW graphs, and retrieves semantically relevant context chunks to ground Groq Cloud LLM responses with source citations.
- **Project 2 (Independent Capstone — Days 4 & 5)**: A fully autonomous Agentic AI system that uses Vector RAG as persistent episodic memory, executes multi-step tool chains in an autonomous ReAct while-loop, self-heals on tool errors, and terminates only when the declared objective is verified as complete.

Day 3 serves as the cognitive bridge: transitioning from passive retrieval to autonomous agency.

---

## 2. The Core Conceptual Reset: Passive Tool Use vs. True Agentic AI

A central prerequisite for this course is dismantling a widespread industry and academic misconception:

> **The Common Misconception**:
> *"If an AI model can read my emails or query a database and summarize it when I ask, it is an Agentic AI."*
>
> **The Reality**:
> That architecture is **Passive Tool Augmentation (Single-Turn Function Calling)**. It is NOT agentic.

### Architectural Comparison

| Dimension | Passive Tool Use / RAG (Not Agentic) | Autonomous Agentic System (True Agency) |
| :--- | :--- | :--- |
| **Control Flow** | Linear request-response pipeline. Single execution pass. | Iterative while-loop (Reason -> Act -> Observe -> Reflect). |
| **Initiative & Goal** | Human decides every step. Model executes single queries. | Human provides high-level objective; model plans and sequences sub-goals. |
| **Error Handling** | If a tool fails, the pipeline crashes or returns an error. | Self-healing: Model inspects error trace, diagnoses failure, repairs arguments, and retries. |
| **Multi-Step Execution** | Cannot chain dependent tasks without hardcoded logic. | Autonomously decomposes complex goals into sub-tasks and executes dynamically. |
| **Memory Utilization** | Context window resets or accumulates raw text logs. | Queries structured Vector RAG memory to recall past actions, preferences, and operational lessons. |
| **Termination Criteria**| Stops when the single prompt completion finishes. | Stops only when the agent verifies that the declared end-state goal has been satisfied. |

---

## 3. Minimum System Requirements (Windows-Native Stack)

This course enforces a strict **zero local GPU / zero local model weights** policy. All inference and embedding services run through standardized cloud API endpoints and lightweight Python libraries on standard student laptops.

### Hardware Requirements
- **Machine**: Windows 10 or Windows 11 laptop (64-bit).
- **RAM**: Minimum 4 GB RAM (8 GB recommended).
- **Storage**: Minimum 5 GB free disk space.
- **Network**: Stable broadband internet access (HTTPS access to `api.groq.com` and `pypi.org`).
- **GPU**: **None required**. No NVIDIA CUDA or dedicated graphics card needed.

### Software Stack (Mandatory)
| Component | Tool | Purpose in Architecture |
| :--- | :--- | :--- |
| **Operating System** | Windows 10/11 | Host environment for all development. |
| **Python** | Python 3.13 (Standard distribution) | Primary execution runtime. Added to PATH. |
| **Package Manager** | `uv` (Fast Python Package Manager) | Fast dependency resolution and environment management. |
| **IDE / Agent Platform** | Antigravity AI-Native IDE | Workspace for agent development, terminal, and debugging. |
| **Version Control** | Git + GitHub | Personal GitHub account required for milestone checkpoints. |
| **Terminal** | PowerShell | Standard Windows terminal. |
| **Inference API** | Groq Cloud API (Free Tier Account) | Cloud LLM inference: Llama 3.3 70B Versatile & Llama 3.1 8B. |
| **Vector Database** | ChromaDB (In-Memory / SQLite persistence) | Local embeddings storage and HNSW cosine similarity search. |

---

## 4. Detailed 5-Day Syllabus

### Day 1: Orientation, Foundations & Vector RAG Architecture

> **Daily Rhythm**: Morning Sessions 1 (`09:30 - 11:00`) & 2 (`11:30 - 13:00`) are **Theory & Live Demos** | Morning Break (`11:00 - 11:30`) | Lunch (`13:00 - 14:00`) | Afternoon Session 3 (`14:00 - 17:00`) is **Hands-On Working Lab**.

#### Session 1 (09:30 - 11:00 — Morning Theory): Orientation & Mental Model Reset
- **09:30 - 10:15: Course Orientation & Icebreaker**
  - Welcome, course outcomes, and student expectation alignment.
  - Interactive survey: Assessing baseline student familiarity with Python, APIs, JSON schemas, and prompt engineering.
  - Discussion of past student projects and common stumbling blocks in AI development.
- **10:15 - 11:00: Deconstructing "Agentic AI" (The Mental Model Reset)**
  - Why current buzzwords confuse tool calling with agency.
  - The spectrum of autonomy:
    - Level 0: Static Prompting (Zero Tools).
    - Level 1: Tool-Augmented LLM / Function Calling (Single-step, human-driven).
    - Level 2: Directed RAG Workflows (Linear retrieval pipelines).
    - Level 3: Autonomous Agents (Dynamic goal decomposition, ReAct loop, self-correction).
    - Level 4: Multi-Agent Collaboration (Specialized agent swarms).
  - The Core Agent Architecture: **Goal + Planner + Memory + Tool Arsenal + Execution Loop**.

- **11:00 - 11:30: Morning Break**

#### Session 2 (11:30 - 13:00 — Morning Theory): Vector Space Geometry, Chunking & Live RAG Demo
- **11:30 - 12:30: Text Embeddings, Distance Geometry & Chunking Science**
  - What is a vector embedding? Mapping discrete text tokens to a continuous $D$-dimensional latent vector space ($\mathbb{R}^{384}$).
  - Mathematical formulation of distance metrics:
    - Dot Product: $\mathbf{u} \cdot \mathbf{v} = \sum_{i=1}^D u_i v_i$
    - Cosine Similarity: $\cos(\theta) = \frac{\mathbf{u} \cdot \mathbf{v}}{\|\mathbf{u}\| \|\mathbf{v}\|}$
    - Euclidean Distance ($L_2$ norm): $d(\mathbf{u}, \mathbf{v}) = \sqrt{\sum_{i=1}^D (u_i - v_i)^2}$
  - Document chunking science: Fixed-size vs. sentence-aware chunking. Sliding window overlaps to prevent boundary context loss.
  - Vector indexing mechanics: Why brute-force search fails at scale ($O(N)$) and how Hierarchical Navigable Small World (HNSW) graphs achieve logarithmic search ($O(\log N)$).
- **12:30 - 13:00: Instructor Live End-to-End RAG Demo**
  - **Instructor Live Demo**: Complete working RAG pipeline querying technical documentation with source citations and safe hallucination refusal.

- **13:00 - 14:00: Lunch Break**

#### Session 3 (14:00 - 17:00 — Working Session): Environment Setup, API Verification & ChromaDB Lab
- **14:00 - 15:30: Environment & API Verification Lab**
  - Installing Python 3.13, Git, and initializing an isolated Python virtual environment using `uv`.
  - Installing base dependencies: `chromadb`, `requests`, `python-dotenv`, `pydantic`, `duckduckgo-search`.
  - Creating safe credential management via `.env` files and `.gitignore` (never hardcoding secrets).
  - Executing `verify.py` to confirm sub-second HTTPS connectivity to Groq API.
- **15:30 - 17:00: ChromaDB Semantic Query Sandbox Lab**
  - Guided lab: Initializing ChromaDB (`chromadb.Client()` / `PersistentClient`), creating collections, inserting text chunks, and running cosine similarity queries with zero overlapping keywords (`chroma_demo.py`).

---

### Day 2: Project 1 — Students Build a Complete Vector RAG System

#### Session 1 (09:30 - 11:00 — Morning Theory): Document Ingestion & Chunking Architecture
- Reading source documents (technical specifications, datasheets, markdown manuals).
- Designing sentence-aware chunking logic with character caps, overlap windows, and metadata injection (`source`, `chunk_index`).
- Designing idempotent ingestion pipelines with `chromadb.PersistentClient`.

- **11:00 - 11:30: Morning Break**

#### Session 2 (11:30 - 13:00 — Morning Theory): Semantic Retrieval & Grounded Prompt Engineering
- Top-$k$ cosine similarity retrieval and cosine distance threshold filtering to discard unrelated noise.
- Prompt template architecture: Injecting retrieved context chunks into the LLM system prompt.
- Enforcing strict grounding constraints: Forbidding hallucination and requiring exact source citation format (`[Source: filename (chunk N)]`).
- Groq Chat Completions API schema (Llama 3.3 70B Versatile) and low-temperature determinism.

- **13:00 - 14:00: Lunch Break**

#### Session 3 (14:00 - 17:00 — Working Session): Build Project 1 (`ingest.py` + `query.py`) & GitHub Push
- **14:00 - 15:45: Hands-On Implementation (`ingest.py` & `query.py`)**
  - Build the ChromaDB ingestion pipeline from the provided knowledge base and verify semantic recall without overlapping keywords.
  - Wire retrieval into Groq Llama 3.3 70B generation with strict citation enforcement.
- **15:45 - 16:30: Edge-Case Verification & Stress Testing**
  - In-domain queries: Grounded accuracy with citations.
  - Out-of-domain queries: Verification that the model admits lack of information.
  - Ambiguous queries: Verifying top-$k$ context handling.
- **16:30 - 17:00: Project 1 Submission Checkpoint**
  - Students push their completed RAG system to GitHub.

---

### Day 3: Bridging RAG to Autonomous Agentic AI with Vector Memory

#### Session 1 (09:30 - 11:00 — Morning Theory): Autonomous ReAct Loops & JSON Tool Calling
- The ReAct cognitive cycle: Thought $\rightarrow$ Action $\rightarrow$ Observation $\rightarrow$ Reflection.
- How LLMs invoke external code: JSON Schema function calling standard (OpenAI/Groq format) and `@register_tool` dynamic dispatch.
- Step budget enforcement (`max_steps = 10`) to prevent infinite execution and billing loops.
- Self-healing error interception design: Catching exceptions and feeding tracebacks back to the LLM as `Observation: Tool Execution Error: <msg>`.

- **11:00 - 11:30: Morning Break**

#### Session 2 (11:30 - 13:00 — Morning Theory): Dual-Memory Architecture, AAR & Capstone Briefing
- Short-Term Working Memory (Context Window & Scratchpad) vs. Long-Term Episodic Memory (ChromaDB Vector Store).
- Designing memory tools: `store_memory(category, observation)` and `recall_memory(query, top_k)`.
- Self-Correction & After Action Review (AAR): Post-execution reflection committing operational constraints to memory.
- **Capstone Briefing**: Disclosure of the 3 Capstone Problem Statements for Project 2; instructor announces the Day 4–5 transition from mentor to strict evaluator.

- **13:00 - 14:00: Lunch Break**

#### Session 3 (14:00 - 17:00 — Working Session): Build `tools.py`, `agent.py`, `memory.py` & `aar_engine.py`
- **14:00 - 16:30: Autonomous Core & Episodic Memory Lab**
  - Implement modular Python tools (`search_web`, calculator, file reader/writer) and the core ReAct while-loop in `agent.py`.
  - Implement `memory.py` (`store_memory` and `recall_memory`) and `aar_engine.py` in pure Python + ChromaDB.
  - Multi-session testing: Verify cross-session recall where lessons saved in Run 1 optimize Run 2.
- **16:30 - 17:00: Capstone Track Selection & Environment Readiness**
  - Students select 1 of the 3 Capstone Problem Statements, stage mock datasets, and verify environments before Day 4.

---

### Days 4 & 5: Project 2 — Independent Capstone Hackathon & Live Defense

Students work independently or in pairs. The instructor does not write code, debug syntax errors, or troubleshoot logic. Students rely on documentation and terminal traces.

#### Day 4: Core Architecture & Tool Pipeline (Unassisted)
- **09:30 - 11:00 (Session 1 — Theory / Standup): Architecture Declaration & Problem Scoping**
  - Declare chosen Problem Statement (IoT, 5G Telecom, or Literature Survey) and draw module block diagram.
- **11:00 - 11:30: Morning Break**
- **11:30 - 13:00 (Session 2 — Theory / Design): Domain Memory Schema & Typed Tool Contracts**
  - Design ChromaDB domain chunk schema, 4 typed JSON tool contracts, path safety rules, and failure-recovery edge cases.
- **13:00 - 14:00: Lunch Break**
- **14:00 - 17:00 (Session 3 — Working): Capstone Build Sprint (`ingest`, 4 Tools & ReAct Loop) & Checkpoint**
  - Ingest mock datasets into ChromaDB, implement all 4 domain tools and the ReAct loop with error interception.
  - **16:30 Checkpoint**: Pass >=3 autonomous tool-call smoke test without crashing and push to GitHub.

#### Day 5: Verification, Benchmarking & Live Defense
- **09:30 - 11:00 (Session 1 — Theory / Audit): Fault-Injection Plan & Rubric Readiness Audit**
  - Design fault-injection tests, audit against the 100-point rubric and zero-point pitfalls, and prepare viva walkthrough.
- **11:00 - 11:30: Morning Break**
- **11:30 - 13:00 (Session 2 — Pre-Defense Working): Stress Testing, Hardening & Documentation**
  - Execute corrupt-input and cross-session memory tests, finalize `trace.jsonl`, `.env.example`, and `README.md`; complete final Git push by 13:00.
- **13:00 - 14:00: Lunch Break**
- **14:00 - 17:00 (Session 3 — Working / Defense): Live Defense, Evaluation & Certification**
  - Each student team runs their agent live against an unseen instructor evaluation benchmark (`14:00 - 16:30`), followed by code walkthrough and oral defense viva questions.
  - **16:30 - 17:00**: Program Retrospective & Certification.

---

## 5. Capstone Engineering Problem Statements (Choose 1 of 3)

### Problem 1: Autonomous IoT Sensor Network Diagnostic Agent (ECE Embedded Systems)
- **Domain**: Embedded Systems, Wireless Sensor Networks, Signal Processing.
- **Scenario**: A campus IoT deployment of 50 multi-modal environmental sensors experiences intermittent telemetry anomalies. The agent is handed an anomaly alert, parses `sensor_logs.csv`, queries historical incident post-mortems in ChromaDB, determines root cause (sensor drift vs. communication dropout vs. battery depletion), and writes an incident audit report.
- **Required Tools**: `query_incident_memory`, `analyze_sensor_telemetry`, `check_network_topology`, `generate_diagnostic_report`.

### Problem 2: Autonomous 5G/Wireless Protocol Compliance Verification Agent (ECE Telecom)
- **Domain**: Telecommunications, Wireless Standards, 3GPP Protocols.
- **Scenario**: A wireless base station firmware build undergoes automated RF testing. The agent receives raw test output logs, extracts measured parameters (EVM, transmit power, frequency offset), evaluates them against 3GPP specification limits, recalls past compliance remediation notes from vector memory, and writes a formal compliance verification report.
- **Required Tools**: `query_compliance_memory`, `parse_test_log`, `verify_against_spec`, `generate_compliance_report`.

### Problem 3: Autonomous Research Literature Survey & Gap Analysis Agent (Academic Core)
- **Domain**: Academic Research, Emerging AI & Hardware Technologies.
- **Scenario**: A student begins an 8th-semester major project on edge AI or neuromorphic architectures. The agent queries a stored corpus of paper abstracts in vector memory, executes live web searches for recent preprints, clusters methodologies, detects unsolved research gaps, and generates an annotated literature review.
- **Required Tools**: `query_literature_memory`, `search_web`, `extract_themes`, `generate_literature_review`.

---

## 6. Evaluation & Grading Rubric (100 Points Total)

| Project & Criterion | Points | Measurable Engineering Requirement |
| :--- | :---: | :--- |
| **P1: Document Ingestion & Chunking** | 10 | Documents correctly chunked on sentence boundaries with metadata; error-free ChromaDB indexing. |
| **P1: Semantic Retrieval Accuracy** | 10 | Relevant chunks retrieved for test queries; irrelevant results filtered using cosine distance. |
| **P1: RAG-Augmented Generation** | 10 | LLM responses grounded in retrieved context with strict source citation notation. |
| **P2: True Agentic Control Flow** | 20 | Pure while-loop (Reason -> Act -> Observe). Hardcoded pipelines score 0 points. |
| **P2: Vector Memory Integration** | 15 | Long-term memory queried contextually. The agent retrieves past records and writes lessons. |
| **P2: Tool Calling & Schema Rigor** | 10 | Minimum 4 tools with valid JSON schemas, typing, and safe execution without crashes. |
| **P2: Self-Healing & Error Recovery** | 10 | When an error occurs, the agent reads the error trace, adjusts its approach, and recovers. |
| **P2: Live Benchmark Defense** | 10 | Agent executes successfully against an unseen evaluation prompt during the Day 5 defense. |
| **P2: Code Quality & Documentation** | 5 | Clean PEP 8 Python, pyproject.toml, .env.example, complete README.md. |

---

## 7. Connecting this Program to Student Career Progression

This program provides undergraduate engineering students with core skills directly transferable to:
1. **VTU Final Year Major Projects (7th/8th Semester)**: Autonomous monitoring agents, intelligent telecom testing suites, and automated research workflows.
2. **Technical Engineering Interviews**: Practical mastery of JSON function calling, embedding geometry, HNSW vector search, and agentic state machines.
3. **Emerging AI Standards**: Direct foundation for Anthropic Model Context Protocol (MCP) and multi-agent swarm orchestration.
