# Autonomous Repo Assistant

An AI-powered CLI chatbot that clones any GitHub repository and answers questions about it — from high-level overviews to line-by-line code explanations — using specialized LLM agents orchestrated through a LangGraph state machine.

---

## Problem Statement

Understanding an unfamiliar codebase is painful. Developers spend hours reading scattered files, tracing data flows, and mentally mapping architecture before they can even ask the right questions.

This tool automates that process. Point it at any public GitHub repo, and ask questions in plain English. Specialized agents handle different types of queries — overview, architecture, data flow, or code explanation — so you get focused, accurate answers without reading a single file yourself.

---

## Features

- **Clone & sync any public GitHub repo** — automatically clones or pulls latest changes
- **Intelligent query routing** — LLM-based router classifies your question and delegates to the right specialist agent
- **Overview agent** — explains what the project does at a high level
- **Architecture agent** — breaks down component boundaries, entry points, and module responsibilities
- **Data flow agent** — traces runtime execution paths and input → output flows
- **Code explainer agent** — reads specific files via MCP tools, summarizes them, and answers detailed code questions
- **File-level caching** — summarized files are cached across turns so repeated questions are instant
- **MCP tool integration** — file reading is handled through a Model Context Protocol server, keeping tool access modular and extensible
- **Interactive CLI REPL** — ask as many questions as you want in a persistent session

---

## Architecture

```
User (CLI REPL)
       │
       ▼
  Orchestrator ──── clones repo, fetches metadata, builds file structure
       │
       ▼
    Router (LLM) ──── classifies question
       │
       ├── analyze_repo ──► Repo Analyzer Sub-Router (LLM)
       │                         │
       │                         ├── overview    ──► Overview Agent    ──► Answer
       │                         ├── architecture──► Architecture Agent──► Answer
       │                         └── dataflow    ──► Data Flow Agent   ──► Answer
       │
       └── explain_code ──► Code Explainer Agent
                                  │
                                  ├── calls MCP get_file tool
                                  ├── passes file to File Summarizer
                                  ├── caches summary
                                  └──► Answer
```

The graph is built with **LangGraph** — each box above is a node, connected via conditional edges based on LLM routing decisions. All agents share a single `State` TypedDict that flows through the graph.

---

## Tech Stack

| Technology | Role |
|---|---|
| Python 3.13+ | Runtime |
| LangGraph | State-machine orchestration for agent flow |
| LangChain + LangChain-Groq | LLM abstraction and Groq API integration |
| Groq API | LLM provider (model: `openai/gpt-oss-20b`) |
| FastMCP | Model Context Protocol server for tool exposure |
| langchain-mcp-adapters | Bridges MCP tools into LangChain tool calling |
| Requests | GitHub REST API calls for repo metadata |
| python-dotenv | Environment variable management |

---

## How to Run

```bash
# 1. Clone this repo
git clone https://github.com/Om-Varma12/journey-to-the-end-of-ai.git
cd "MCP/Project 2 - EASY - Autonomous-Repo-Assistant"

# 2. Create and activate a virtual environment
python -m venv .venv

# Windows
.venv\Scripts\Activate.ps1

# macOS/Linux
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
# Create a .env file in the project root with:
GROQ_API_KEY=your_groq_api_key_here

# 5. Run the assistant
python -m graph.orchestrator
```

You will be prompted to enter a GitHub username and repository name. Once cloned, the REPL starts — type any question about the repo and get an answer.

---

## Project Structure

```
├── agents/                  # All LLM agent definitions
│   ├── router.py            # Main query classifier (analyze_repo | explain_code)
│   ├── repo_analyzer_router.py  # Sub-classifier (overview | architecture | dataflow)
│   ├── overview_agent.py    # High-level repo summary agent
│   ├── arch_agent.py        # Architecture breakdown agent
│   ├── data_flow_agent.py   # Runtime data flow tracing agent
│   ├── code_explainer.py    # File-level code explanation with MCP tool calling
│   └── file_summarizer_agent.py  # Compresses raw file content into structured summaries
├── graph/                   # LangGraph orchestration
│   ├── orchestrator.py      # Entry point — repo setup, graph construction, REPL loop
│   ├── nodes.py             # Node functions wiring agents to the graph
│   └── state.py             # Shared state TypedDict definition
├── mcp_server/              # Model Context Protocol server
│   ├── server.py            # FastMCP server setup
│   └── tools/
│       ├── file_tools.py    # get_file tool — reads files from cloned repos
│       ├── repo_tools.py    # (placeholder for future repo-level tools)
│       └── search_tools.py  # (placeholder for future search tools)
├── prompts/                 # All prompt templates (one per agent)
├── services/                # Non-LLM utility services
│   ├── repo_service.py      # Git clone/pull, GitHub API, file structure builder
│   └── file_service.py      # Simple file reader utility
├── cli/                     # (placeholder for future CLI module)
├── repos/                   # Cloned repositories are stored here
└── tests/                   # (placeholder for future tests)
```

---

## Tradeoffs & Limitations

- **Single MCP tool** — only `get_file` is implemented; agents must know exact file paths from the structure. No search or grep capability yet.
- **No error handling** — network failures, malformed LLM responses, or missing files will crash the app.
- **Prompt-based routing** — routers rely on the LLM returning an exact label string. No fallback if the response is unexpected.
- **No conversation memory** — file cache persists across turns, but there is no chat history. Each question is treated independently.
- **No streaming** — responses are fully awaited before displaying, so there is a noticeable wait on longer answers.
- **Unauthenticated GitHub API** — rate-limited to 60 requests per hour. Private repos are not supported.
- **No tests** — the test directory exists but contains no test files yet.
- **Model is hardcoded** — uses `openai/gpt-oss-20b` via Groq; switching models requires a code change.

---

## Future Improvements

- Add search and grep MCP tools for smarter file discovery
- Implement conversation memory for multi-turn reasoning
- Add streaming for real-time response output
- Build error handling and graceful fallbacks for routing failures
- Support authenticated GitHub API for private repos and higher rate limits
- Make the LLM model configurable via environment variables
- Add a web UI or API layer alongside the CLI
- Write tests for agents, routing logic, and MCP tools
