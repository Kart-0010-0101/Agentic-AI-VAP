# VAP Implementation Plan: 5-Day Agentic AI Workshop

This document serves as the complete structured guide for generating the workshop PDF. It contains all content in sequential order: title page metadata, syllabus, project specifications, day-by-day implementation steps, code templates, evaluation criteria, and instructor notes.

---

## Document Structure (PDF Layout Order)

```
1. Title Page
2. Table of Contents
3. Course Overview & Syllabus
4. System Requirements & Environment Setup Guide
5. Day 1: Orientation, Foundations & RAG Architecture
6. Day 2: Project 1 — Build a Complete RAG System
7. Day 3: From Passive RAG to Autonomous Agentic AI
8. Day 4: Project 2 — Independent Capstone (Day 1 of 2)
9. Day 5: Project 2 — Capstone Defense (Day 2 of 2)
10. Appendix A: Capstone Problem Statements (Full Specifications)
11. Appendix B: Evaluation Rubric
12. Appendix C: Pre-Workshop Setup Guide for Students
13. Appendix D: Recommended Reading & References
```

---

## 1. Title Page

- **Document Title**: Engineering Autonomous Agentic AI Systems with Vector RAG Memory
- **Subtitle**: 5-Day Value Added Program (VAP) — Complete Workshop Guide
- **Target Audience**: ECE 5th Semester, 3rd Year
- **Institution**: [College Name — to be filled by instructor]
- **Department**: Department of Electronics and Communication Engineering
- **Instructor**: [Instructor Name — to be filled]
- **Duration**: 5 Days (Full-Time Intensive Workshop)
- **Academic Year**: 2026-2027

---

## 2. Course Overview

### Learning Objectives

Upon completion of this 5-day program, students will be able to:

1. Distinguish between passive tool-augmented LLM applications and autonomous agentic AI architectures.
2. Design and implement a Vector RAG pipeline: document ingestion, chunking, embedding generation, vector storage in ChromaDB, and semantic retrieval.
3. Build an autonomous agent execution loop using the ReAct pattern (Reason + Act) with dynamic tool dispatch and error self-correction.
4. Integrate Vector RAG as persistent episodic memory into an autonomous agent, enabling cross-session knowledge recall and operational learning.
5. Independently architect, implement, test, and defend a complete Agentic AI system against unseen evaluation scenarios.

### Two-Project Progression

| Project | Type | Days | Description |
| :--- | :--- | :--- | :--- |
| **Project 1** | Guided Build | Day 1 (Session 2-3) + Day 2 | Basic Vector RAG System. Instructor demonstrates a working RAG pipeline first; students then build their own from scratch. |
| **Project 2** | Independent Capstone | Day 4 + Day 5 | Autonomous Agentic AI System with Vector RAG Memory. Students select 1 of 3 problem statements and build without instructor assistance. |

Day 3 serves as the bridge: transitioning from passive RAG to autonomous agentic architecture through guided instruction.

---

## 3. System Requirements & Environment Setup

### Hardware
- Windows 10/11 laptop
- Minimum 4 GB RAM (8 GB recommended)
- 5 GB free disk space
- Stable internet connection
- No GPU required

### Software Installation Steps

#### Step 1: Install Python 3.13
1. Download from https://www.python.org/downloads/
2. Run installer. CHECK "Add python.exe to PATH" before clicking Install.
3. Verify: Open PowerShell, run `python --version`. Expected output: `Python 3.13.x`.

#### Step 2: Install uv (Package Manager)
```powershell
pip install uv
uv --version
```

#### Step 3: Install Git for Windows
1. Download from https://git-scm.com/download/win
2. Install with default options.
3. Configure:
```powershell
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

#### Step 4: Create GitHub Account
1. Sign up at https://github.com
2. Create a new repository named `vap-agentic-ai`.

#### Step 5: Install Antigravity IDE
1. Download from https://antigravity.dev
2. Install and launch.

#### Step 6: Obtain Groq API Key
1. Go to https://console.groq.com
2. Sign up (free, no credit card required).
3. Navigate to API Keys and create a new key.
4. Save the key securely. Never commit it to Git.

#### Step 7: Project Initialization
```powershell
mkdir vap-agentic-ai
cd vap-agentic-ai
uv init
uv add chromadb requests python-dotenv pydantic duckduckgo-search
```

#### Step 8: Credential Setup
Create a `.env` file in the project root:
```
GROQ_API_KEY=gsk_your_key_here
```

Create a `.gitignore` file:
```
.env
__pycache__/
*.pyc
.venv/
```

#### Step 9: API Connectivity Verification
Create `verify.py`:
```python
import os
import json
import urllib.request
from dotenv import load_dotenv

load_dotenv()

url = "https://api.groq.com/openai/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {os.environ['GROQ_API_KEY']}",
    "Content-Type": "application/json",
}
body = json.dumps({
    "model": "llama-3.1-8b-instant",
    "messages": [{"role": "user", "content": "Say hello in one word."}],
    "max_tokens": 10,
}).encode()

req = urllib.request.Request(url, data=body, headers=headers)
with urllib.request.urlopen(req) as resp:
    result = json.loads(resp.read())
    print("API Connected:", result["choices"][0]["message"]["content"])
```
Run: `uv run python verify.py`

---

## 4. Day 1: Orientation, Foundations & RAG Architecture

### Session 1: Morning Theory (09:30 - 11:00)

#### 4.1 Course Orientation & Icebreaker (09:30 - 10:15)
- Welcome and introductions.
- Student skill survey: Python familiarity, API experience, prior AI/ML exposure.
- Open discussion: "What do you think an AI agent is?" — Collect responses on whiteboard.
- Course roadmap walkthrough: 2 projects, 5 days, what "done" looks like.

#### 4.2 The Mental Model Reset (10:15 - 11:00)

**Key Teaching Points**:

The spectrum of AI system autonomy:

| Level | Architecture | Example | Agentic? |
| :---: | :--- | :--- | :---: |
| 0 | Static Prompting | ChatGPT with no tools | No |
| 1 | Function Calling | LLM calls `get_weather()` when asked | No |
| 2 | RAG Pipeline | LLM retrieves documents before answering | No |
| 3 | Autonomous Agent | LLM plans steps, calls tools in a loop, self-corrects | Yes |
| 4 | Multi-Agent Swarm | Multiple specialized agents collaborating | Yes |

**Critical Distinction** (write on board):
> "If a human wrote the control flow and the AI just fills in text, it is NOT agentic. If the AI decides WHAT to do next based on WHAT it observed, it IS agentic."

**The Agent Architecture Diagram** (draw on board):
```
User Goal --> [PLANNER] --> [TOOL EXECUTOR] --> [ENVIRONMENT]
                 ^                                    |
                 |            [MEMORY STORE]          |
                 +--- [REFLECTOR] <-- Observation <---+
```

### Session 2: Morning Theory (11:30 - 13:00)

#### 4.3 Vector Embeddings Deep Dive (11:30 - 12:10)

**Teaching Points**:
- A text embedding converts a sentence into a list of numbers (a vector) that captures its meaning.
- Semantically similar sentences produce vectors that are close together in vector space.
- Cosine similarity: Measures the angle between two vectors. 1.0 = identical meaning, 0.0 = unrelated.

**Live Demonstration** (previewed by instructor in Session 2; run hands-on by students in Session 3):
```python
import chromadb

client = chromadb.Client()
collection = client.create_collection("demo")

# Add documents
collection.add(
    documents=[
        "The MOSFET gate voltage controls the drain current.",
        "A capacitor stores energy in an electric field.",
        "Python is a programming language used for AI.",
    ],
    ids=["doc1", "doc2", "doc3"],
)

# Query
results = collection.query(
    query_texts=["How does a transistor work?"],
    n_results=2,
)
print(results["documents"])
# Expected: Returns doc1 (MOSFET) as top result — semantic match, not keyword match.
```

**Key Insight**: The query "How does a transistor work?" contains zero words in common with "The MOSFET gate voltage controls the drain current" — yet vector similarity correctly identifies it as the most relevant document.

#### 4.4 Document Chunking Strategies (12:10 - 12:35)

**Teaching Points**:
- Large documents must be split into chunks before embedding. An entire textbook chapter as one vector loses semantic precision.
- Fixed-size chunking: Split every N characters with overlap. Simple but can break mid-sentence.
- Sentence-based chunking: Split on sentence boundaries. Preserves meaning.
- Metadata tagging: Each chunk carries metadata (source file, section, page number) for traceability.

**Code Template — Simple Sentence Chunker**:
```python
def chunk_text(text: str, max_chars: int = 500) -> list[dict]:
    sentences = text.replace("\n", " ").split(". ")
    chunks, current, start_idx = [], "", 0
    for sentence in sentences:
        if len(current) + len(sentence) > max_chars and current:
            chunks.append({"text": current.strip(), "index": start_idx})
            start_idx += 1
            current = sentence + ". "
        else:
            current += sentence + ". "
    if current.strip():
        chunks.append({"text": current.strip(), "index": start_idx})
    return chunks
```

#### 4.5 Instructor RAG Demo (12:35 - 13:00)

**Instructor demonstrates a complete working RAG system end-to-end** (Lunch Break follows `13:00 - 14:00`):
- Ingesting sample electronics manuals, retrieving top-$k$ chunks, calling Groq Llama 3.3 70B with strict grounding, and showing clean out-of-domain refusals.

### Session 3: Afternoon Working Lab (14:00 - 17:00)

#### 4.6 Environment Setup & ChromaDB Verification Lab (14:00 - 17:00)
- Walk through Steps 1-9 from Section 3 above (`14:00 - 15:30`).
- Every student must have a working `verify.py` output before moving to the vector sandbox.
- Troubleshoot common issues: PATH not set, corporate proxy blocking API calls, `.env` not loaded.
- Run the live `chroma_demo.py` semantic search lab (`15:30 - 17:00`) using `chromadb.Client()` / `PersistentClient`.

1. Ingest a knowledge base (e.g., 20 electronics troubleshooting entries) into ChromaDB.
2. Accept a user query.
3. Retrieve top-3 relevant chunks.
4. Inject retrieved context into the LLM prompt.
5. Generate a grounded response with source citations.

Students observe and ask questions. They do NOT code this yet — they build it themselves on Day 2.

---

## 5. Day 2: Project 1 — Students Build a Complete RAG System

### Project 1 Specification

**Objective**: Build a complete RAG pipeline that ingests a provided knowledge base into ChromaDB, accepts natural language queries, retrieves relevant context, and generates LLM responses grounded in the retrieved documents.

**Deliverables**:
- `ingest.py`: Reads source documents, chunks them, and stores embeddings in ChromaDB.
- `query.py`: Accepts a user query, retrieves relevant chunks, calls the Groq API with augmented context, and prints the response with source citations.
- `knowledge_base/`: Directory containing the source documents.

### Session 1: Morning Theory (09:30 - 11:00)

#### 5.1 Document Ingestion & Chunking Architecture (09:30 - 11:00)

Students study the `ingest.py` architecture and design `load_documents()` + `chunk_document()`:

```python
# ingest.py — Skeleton for students to complete
import os
import chromadb

def load_documents(directory: str) -> list[dict]:
    """Read all .md or .txt files from the knowledge base directory."""
    docs = []
    for filename in os.listdir(directory):
        if filename.endswith((".md", ".txt")):
            path = os.path.join(directory, filename)
            with open(path, "r", encoding="utf-8") as f:
                docs.append({"filename": filename, "content": f.read()})
    return docs

def chunk_document(doc: dict, max_chars: int = 500) -> list[dict]:
    """Split a document into chunks with metadata."""
    # TODO: Students implement chunking logic here
    pass

def ingest(directory: str = "knowledge_base"):
    """Main ingestion pipeline."""
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_or_create_collection("rag_knowledge")

    raw_docs = load_documents(directory)
    for doc in raw_docs:
        chunks = chunk_document(doc)
        for chunk in chunks:
            collection.add(
                documents=[chunk["text"]],
                metadatas=[{"source": doc["filename"], "chunk_index": chunk["index"]}],
                ids=[f"{doc['filename']}_chunk_{chunk['index']}"],
            )
    print(f"Ingested {collection.count()} chunks into ChromaDB.")

if __name__ == "__main__":
    ingest()
```

### Session 2: Morning Theory (11:30 - 13:00)

#### 5.2 Semantic Retrieval & Grounded Prompt Architecture (11:30 - 13:00)

Design `query.py` retrieval filtering (`max_distance`), strict grounding prompt rules, and Groq API schema before Lunch (`13:00 - 14:00`):

```python
# query.py — Skeleton for students to complete
import os
import json
import urllib.request
import chromadb
from dotenv import load_dotenv

load_dotenv()

def retrieve(query: str, top_k: int = 3) -> list[dict]:
    """Retrieve top-k relevant chunks from ChromaDB."""
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_collection("rag_knowledge")
    results = collection.query(query_texts=[query], n_results=top_k)
    # TODO: Students format results with metadata
    return results

def generate_response(query: str, context_chunks: list) -> str:
    """Call Groq API with retrieved context."""
    # TODO: Students build the prompt template and API call
    pass

if __name__ == "__main__":
    user_query = input("Enter your question: ")
    # TODO: Students wire retrieve() -> generate_response() -> print
```

### Session 3: Afternoon Working Lab (14:00 - 17:00)

#### 5.3 End-to-End RAG Implementation (`ingest.py` + `query.py`) (14:00 - 15:45)

Students build and test the complete ingestion and Groq LLM generation pipeline:

**Prompt Template Pattern**:
```
You are a knowledgeable technical assistant. Answer the user's question
using ONLY the provided context. If the context does not contain the answer,
say "I don't have enough information to answer that."

Cite your sources using [Source: filename] notation.

Context:
{retrieved_chunks}

Question: {user_query}
```

**Groq API Call Pattern**:
```python
def call_groq(messages: list[dict]) -> str:
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.environ['GROQ_API_KEY']}",
        "Content-Type": "application/json",
    }
    body = json.dumps({
        "model": "llama-3.3-70b-versatile",
        "messages": messages,
        "max_tokens": 1024,
        "temperature": 0.2,
    }).encode()
    req = urllib.request.Request(url, data=body, headers=headers)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())["choices"][0]["message"]["content"]
```

#### 5.4 Testing & Edge Cases (15:45 - 16:30)

Test scenarios students must verify:
1. **In-domain query**: Query about a topic covered in the knowledge base. Expected: Accurate, cited response.
2. **Out-of-domain query**: Query about something NOT in the knowledge base. Expected: "I don't have enough information."
3. **Ambiguous query**: Vague query that partially matches multiple chunks. Expected: Response acknowledges ambiguity or presents multiple perspectives.

#### 5.5 Project 1 Submission (16:30 - 17:00)

```powershell
git add .
git commit -m "Project 1: Complete RAG system with ChromaDB"
git push origin main
```

**Instructor Closing Point**:
> "You have built a powerful retrieval-augmented system. But notice: YOU typed the query. YOU initiated every interaction. The system did exactly one thing — retrieve and generate — then stopped. It has no goals, no planning, no error recovery, and no memory of past sessions. Tomorrow, we make it autonomous."

---

## 6. Day 3: From Passive RAG to Autonomous Agentic AI

### Session 1: Morning Theory (09:30 - 11:00)

#### 6.1 The ReAct Pattern, Tool Schemas & While-Loop Design (09:30 - 11:00)

**Teaching Points**:

The ReAct loop is the core control structure of an autonomous agent:

```
while not goal_achieved and steps < max_steps:
    1. THINK  — LLM reasons about current state and decides next action
    2. ACT    — Execute the chosen tool with generated arguments
    3. OBSERVE — Capture tool output (or error message)
    4. REFLECT — LLM evaluates: Did this succeed? What next?
```

**Tool Definition Schema** (teach students the format LLMs expect):
```python
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Search the web for current information on a topic.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query string.",
                    }
                },
                "required": ["query"],
            },
        },
    },
]
```

#### 6.2 Agent While-Loop Architecture (`agent.py`) (Theory Design)

**Core Agent Loop — Architectural Specification (implemented hands-on in Session 3)**:

```python
# agent.py — The autonomous agent core
import json
import os
import urllib.request
from dotenv import load_dotenv

load_dotenv()

MAX_ITERATIONS = 10

# Tool registry — maps tool names to Python functions
TOOL_REGISTRY = {}

def register_tool(func):
    """Decorator to register a function as an agent tool."""
    TOOL_REGISTRY[func.__name__] = func
    return func

@register_tool
def search_web(query: str) -> str:
    from duckduckgo_search import DDGS
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=3))
    return json.dumps(results, indent=2) if results else "No results found."

@register_tool
def read_file(filepath: str) -> str:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()[:2000]  # ponytail: cap to prevent context explosion
    except FileNotFoundError:
        return f"Error: File '{filepath}' not found."

@register_tool
def write_file(filepath: str, content: str) -> str:
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return f"Successfully wrote {len(content)} characters to {filepath}."

@register_tool
def calculate(expression: str) -> str:
    try:
        # ponytail: ast.literal_eval is safer but eval with restricted builtins works for math
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)
    except Exception as e:
        return f"Calculation error: {e}"


def call_llm(messages: list[dict], tools: list[dict] | None = None) -> dict:
    """Call Groq API with optional tool definitions."""
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.environ['GROQ_API_KEY']}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": messages,
        "max_tokens": 1024,
        "temperature": 0.1,
    }
    if tools:
        payload["tools"] = tools
        payload["tool_choice"] = "auto"

    body = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=body, headers=headers)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def run_agent(goal: str):
    """Execute the autonomous agent loop."""
    system_prompt = (
        "You are an autonomous AI agent. You have access to tools. "
        "Think step by step about how to achieve the user's goal. "
        "Use tools when needed. When the goal is fully achieved, "
        "respond with FINAL ANSWER: followed by your complete response."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": goal},
    ]

    # Build tool schemas from registry
    tool_schemas = []  # TODO: Students generate schemas from TOOL_REGISTRY

    for step in range(MAX_ITERATIONS):
        print(f"\n--- Step {step + 1} ---")
        response = call_llm(messages, tools=tool_schemas)
        choice = response["choices"][0]
        message = choice["message"]

        # Check if the agent wants to call a tool
        if message.get("tool_calls"):
            messages.append(message)
            for tool_call in message["tool_calls"]:
                func_name = tool_call["function"]["name"]
                func_args = json.loads(tool_call["function"]["arguments"])
                print(f"Action: {func_name}({func_args})")

                # Execute the tool
                if func_name in TOOL_REGISTRY:
                    try:
                        result = TOOL_REGISTRY[func_name](**func_args)
                    except Exception as e:
                        result = f"Tool execution error: {e}"
                else:
                    result = f"Error: Unknown tool '{func_name}'."

                print(f"Observation: {result[:200]}...")
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call["id"],
                    "content": result,
                })
        else:
            # No tool call — check if agent is done
            content = message.get("content", "")
            if "FINAL ANSWER:" in content:
                print(f"\nAgent completed in {step + 1} steps.")
                print(content)
                return content
            else:
                messages.append(message)

    print("Agent reached maximum iterations without completing the goal.")


if __name__ == "__main__":
    user_goal = input("Enter goal for the agent: ")
    run_agent(user_goal)
```

### Session 2: Morning Theory (11:30 - 13:00)

#### 6.3 Dual Memory & Vector RAG as Episodic Memory (`memory.py`) (11:30 - 12:30)

**Teaching Points**:
- The RAG system from Project 1 becomes a TOOL that the agent can call.
- Two new tools added to the agent's arsenal:

```python
import chromadb

memory_client = chromadb.PersistentClient(path="./agent_memory")
memory_collection = memory_client.get_or_create_collection("episodic_memory")

@register_tool
def store_memory(category: str, observation: str) -> str:
    """Store an observation into long-term vector memory."""
    doc_id = f"mem_{memory_collection.count()}"
    memory_collection.add(
        documents=[observation],
        metadatas=[{"category": category}],
        ids=[doc_id],
    )
    return f"Stored memory: '{observation[:80]}...' under category '{category}'."

@register_tool
def recall_memory(query: str, top_k: int = 3) -> str:
    """Recall relevant past observations from long-term vector memory."""
    if memory_collection.count() == 0:
        return "No memories stored yet."
    results = memory_collection.query(query_texts=[query], n_results=min(top_k, memory_collection.count()))
    memories = []
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        memories.append(f"[{meta['category']}] {doc}")
    return "\n".join(memories) if memories else "No relevant memories found."
```

**Updated System Prompt** (agent now knows it has memory):
```
You are an autonomous AI agent with persistent memory.
Before starting a complex task, use recall_memory to check if you have
solved similar problems before. After completing important steps, use
store_memory to save key findings for future reference.
```

#### 6.4 Self-Correction, After Action Review & Capstone Briefing (12:30 - 13:00)

**Teaching the AAR Pattern**:

After the agent completes (or fails) a task, append a reflection step:

```python
def after_action_review(goal: str, steps_taken: list, outcome: str):
    """Generate and store a lessons-learned entry."""
    review_prompt = f"""Review this agent execution:
Goal: {goal}
Steps taken: {json.dumps(steps_taken, indent=2)}
Outcome: {outcome}

What went well? What failed? What rule should the agent follow next time?
Provide a single concise lesson in one sentence."""

    messages = [{"role": "user", "content": review_prompt}]
    response = call_llm(messages)
    lesson = response["choices"][0]["message"]["content"]
    store_memory("aar_lesson", lesson)
    return lesson
```

### Session 3: Afternoon Working Lab (14:00 - 17:00)

#### 6.5 Autonomous Agent, Memory & AAR Implementation + Capstone Prep (14:00 - 17:00)

- Build `tools.py`, `agent.py` (with `max_steps=10` and `try/except` traceback feedback), `memory.py` (`store_memory` / `recall_memory`), and `after_action_review()`.
- Run multi-session test proving Run 2 recalls the AAR lesson from Run 1.
- Distribute the 3 problem statements (see Section 8 below) and stage capstone mock datasets (`16:30 - 17:00`).
- Students select one problem statement and verify all environments are ready.
- Instructor announces: "Starting tomorrow at 09:30, I am an evaluator only. No code help."

---

## 7. Days 4 & 5: Project 2 — Independent Capstone

### Day 4: Architecture & Core Loop (Unassisted)

| Time | Session | Activity |
| :--- | :--- | :--- |
| 09:30 - 11:00 | Session 1 (Theory / Standup) | Standup: Declare chosen problem statement and draw system block diagram. |
| 11:00 - 11:30 | Morning Break | — |
| 11:30 - 13:00 | Session 2 (Theory / Design) | Design ChromaDB domain schema, 4 typed tool contracts, path safety & edge cases. |
| 13:00 - 14:00 | Lunch Break | — |
| 14:00 - 17:00 | Session 3 (Working Sprint) | Ingest domain data, code 4 tools + ReAct loop; `16:30` smoke test (>=3 tool calls) & Git push. |

### Day 5: Testing, Documentation & Live Defense

| Time | Session | Activity |
| :--- | :--- | :--- |
| 09:30 - 11:00 | Session 1 (Theory / Audit) | Fault-injection test plan, 100-point rubric audit, zero-point pitfalls & viva prep. |
| 11:00 - 11:30 | Morning Break | — |
| 11:30 - 13:00 | Session 2 (Pre-Defense Working) | Corrupt-input & cross-session recall tests, finalize `trace.jsonl` & README; `13:00` Git push. |
| 13:00 - 14:00 | Lunch Break | — |
| 14:00 - 17:00 | Session 3 (Live Defense) | Execute agent against unseen benchmark (`14:00 - 16:30`), viva Q&A & certification (`16:30 - 17:00`). |

---

## 8. Capstone Problem Statements (Choose 1 of 3)

### Problem Statement 1: Autonomous IoT Sensor Network Diagnostic Agent

**Domain**: ECE Core — Embedded Systems, Sensor Networks, Signal Processing.

**Scenario**: A campus IoT deployment of 50 environmental sensors (temperature, humidity, air quality) is experiencing intermittent data anomalies. The agent is provided with historical sensor telemetry logs and past incident post-mortems stored in vector memory. Given a new anomaly alert, the agent must autonomously diagnose root cause (sensor drift, communication dropout, power supply degradation, or environmental interference), consult past resolutions from memory, and generate a structured diagnostic report.

**Required Tools**:
1. `query_incident_memory` — Semantic retrieval of similar past sensor incidents from ChromaDB.
2. `analyze_sensor_telemetry` — Reads mock sensor data logs (CSV/JSON), computes statistical anomalies (mean, standard deviation, spike detection).
3. `check_network_topology` — Queries a mock network graph to identify communication path failures.
4. `generate_diagnostic_report` — Writes a structured Markdown report with root cause analysis and recommended actions.

**Provided Mock Data**: `sensor_logs.csv` (500 rows of timestamped sensor readings with injected anomalies), `past_incidents.json` (15 historical incident records), `network_topology.json` (sensor node connectivity graph).

---

### Problem Statement 2: Autonomous 5G/Wireless Protocol Compliance Verification Agent

**Domain**: ECE Core — Telecommunications, Wireless Systems, Protocol Standards.

**Scenario**: A wireless device manufacturer needs to verify that their 5G NR base station firmware complies with 3GPP specification parameters. The agent is provided with protocol specification excerpts and past compliance test results in vector memory. Given a new firmware test log, the agent must extract measured parameters, compare them against specification thresholds, identify violations, recall how similar violations were resolved in prior versions, and produce a compliance verification report.

**Required Tools**:
1. `query_compliance_memory` — Semantic retrieval of past compliance outcomes and resolution notes.
2. `parse_test_log` — Reads firmware test output logs, extracts measured RF parameters.
3. `verify_against_spec` — Compares extracted parameters against specification thresholds, flags violations.
4. `generate_compliance_report` — Writes a structured pass/fail compliance report.

**Provided Mock Data**: `firmware_test_output.json` (50 measured RF parameters), `3gpp_spec_thresholds.json` (specification limits), `past_compliance_tests.json` (20 historical test records with resolutions).

---

### Problem Statement 3: Autonomous Research Literature Survey & Gap Analysis Agent

**Domain**: Universal Academic Skill — Directly Useful for Final Year Projects.

**Scenario**: A student is beginning a project on a specified technical topic (e.g., "Federated Learning for Edge IoT Devices" or "Neuromorphic Computing Architectures"). The agent is provided with a corpus of research paper abstracts stored in vector memory. Given a research question, the agent must survey the stored literature, identify key themes and methodologies, detect research gaps, and generate a structured literature review with citations and a proposed research direction.

**Required Tools**:
1. `query_literature_memory` — Semantic retrieval of relevant paper abstracts and findings.
2. `search_web` — Searches the web for additional recent references not in the local corpus.
3. `extract_themes` — Clusters retrieved papers by methodology and application domain to identify trends and gaps.
4. `generate_literature_review` — Writes a structured Markdown literature review with thematic sections and identified gaps.

**Provided Mock Data**: `paper_abstracts.json` (40 research paper abstracts with title, authors, year, abstract, methodology, and key findings).

---

## 9. Evaluation Rubric

### Project 1: Basic RAG System (30 Points)

| Category | Max Score | Criteria |
| :--- | :---: | :--- |
| Document Ingestion & Chunking | 10 | Documents correctly chunked with metadata and stored in ChromaDB. |
| Semantic Retrieval Accuracy | 10 | Relevant chunks retrieved for test queries; irrelevant results filtered. |
| RAG-Augmented Generation | 10 | LLM responses grounded in retrieved context with source citations. |

### Project 2: Agentic AI with Vector RAG Memory (70 Points)

| Category | Max Score | Criteria |
| :--- | :---: | :--- |
| True Agentic Control Flow | 20 | Autonomous while-loop (Reason -> Act -> Observe). Hardcoded execution order = 0 points. |
| Vector RAG Memory Integration | 15 | Long-term memory queried contextually; past records integrated into reasoning. |
| Tool Calling & Schema Rigor | 10 | Robust JSON schemas, strict typing, reliable execution of all required tools. |
| Self-Healing & Error Recovery | 10 | Agent reads errors, adjusts approach, and recovers autonomously. |
| Live Defense & Benchmark Test | 10 | Agent executes against unseen evaluation prompt during Day 5 defense. |
| Code Quality & Documentation | 5 | PEP 8, zero hardcoded credentials, clean pyproject.toml, README. |

---

## 10. Recommended Daily Schedule

| Time | Session | Mode |
| :--- | :--- | :--- |
| 09:30 - 11:00 | Session 1: Concepts, Architecture & Design Theory | Morning Theory |
| 11:00 - 11:30 | Morning Refreshment Break | Break |
| 11:30 - 13:00 | Session 2: Deep Dive, Grounding Rules & Live Demos | Morning Theory |
| 13:00 - 14:00 | Lunch Break | Break |
| 14:00 - 17:00 | Session 3: Hands-On Coding, Testing & GitHub Checkpoints | Working Session |

---

## 11. Instructor Preparation Checklist

- [ ] Confirm lab has unrestricted HTTPS access to `api.groq.com` and `pypi.org`.
- [ ] Distribute pre-workshop guide: Python 3.13 install, Git for Windows, GitHub account.
- [ ] Prepare knowledge base documents for Project 1 RAG ingestion.
- [ ] Prepare mock datasets for each of the 3 capstone problem statements.
- [ ] Prepare unseen evaluation prompts for Day 5 live defense.
- [ ] Verify Groq API free-tier signup is accessible from campus network.
- [ ] Print evaluation rubric sheets for Day 5.

---

## 12. References & Recommended Reading

1. Yao, S. et al. (2023). "ReAct: Synergizing Reasoning and Acting in Language Models." ICLR 2023.
2. Lewis, P. et al. (2020). "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks." NeurIPS 2020.
3. ChromaDB Documentation: https://docs.trychroma.com
4. Groq API Documentation: https://console.groq.com/docs
5. Python 3.13 Documentation: https://docs.python.org/3.13/
