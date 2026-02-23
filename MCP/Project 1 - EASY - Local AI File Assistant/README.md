# 🗂️ Local AI File Assistant (MCP + LangGraph)

A local AI-powered file assistant built with MCP, LangChain/LangGraph, and Groq LLM.

## Project Structure
```
.
├── server.py        # MCP file system server
├── client.py        # LangGraph agent client
├── requirements.txt
├── .env
└── README.md
```

## Setup

### 1. Install uv
```bash
pip install uv
uv --version
```

### 2. Initialize Project
```bash
uv init
```

### 3. Install Dependencies
```bash
uv add langgraph langchain langchain-groq langchain-mcp-adapters mcp python-dotenv
```

### 4. Configure Environment

Create a `.env` file:
```
GROQ_API_KEY=your_groq_api_key_here
```

## Running
```bash
uv run client.py
```

The client automatically spawns the MCP server as a subprocess.

## Example Usage
```
You: set the folder directory to this path: D:\Projects\testing
You: list files
You: read the file example.txt
You: write a new file called new.txt with content "Hello world"
```

## Architecture
```
User → LangGraph Agent (LLM) → MCP Client → MCP Server → Local File System
```

## Available Tools

| Tool | Description |
|------|-------------|
| `set_folder_location(path)` | Set working directory |
| `list_files()` | List files in current directory |
| `read_file(filename)` | Read a file's contents |
| `write_file(filename, content)` | Write content to a file |

## Notes

- `ROOT_DIR` state persists for the lifetime of the server process
- MCP server uses `stdio` transport
- LLM never directly accesses the filesystem — all operations go through MCP tools
- Without memory enabled, the agent won't remember previous chat context

## Troubleshooting

**"Connection closed"** — Ensure `server.py` ends with `if __name__ == "__main__": mcp.run()` and you're running via `uv run client.py`.

**Groq model errors** — Verify your `GROQ_API_KEY` is valid and you're using a supported model name.