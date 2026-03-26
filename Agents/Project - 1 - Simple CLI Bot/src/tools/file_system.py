# src/tools/file_system.py
import os
from pathlib import Path
from src.types import Tool, ToolDefinition


# ── Sandboxing ─────────────────────────────────────────────────────────────────
# The agent can only touch files inside ./workspace.
# Path traversal like "../../etc/passwd" gets caught by the check below.
# This is your first real taste of tool security — you'll go much deeper in P3 + P5.

WORKSPACE = Path("./workspace").resolve()
WORKSPACE.mkdir(parents=True, exist_ok=True)


def _safe_path(user_path: str) -> Path:
    resolved = (WORKSPACE / user_path).resolve()
    # resolve() normalises ".." — so "../../../etc/passwd" becomes "/etc/passwd"
    # which does NOT start with WORKSPACE, so we block it.
    if not str(resolved).startswith(str(WORKSPACE)):
        raise ValueError(
            f'"{user_path}" resolves outside the workspace. '
            f'Only paths inside ./workspace are allowed.'
        )
    return resolved


# ── Read ───────────────────────────────────────────────────────────────────────

def _read(input: dict) -> str:
    try:
        file_path = _safe_path(input["path"])
    except ValueError as e:
        return f"Error: {e}"

    if not file_path.exists():
        return f'File not found: "{input["path"]}"'

    content = file_path.read_text(encoding="utf-8")

    # Guard against blowing the context window with a huge file
    if len(content) > 40_000:
        return (
            f"[File is large: {len(content)} chars. Showing first 40,000]\n\n"
            + content[:40_000]
        )

    return content


file_read_tool = Tool(
    definition=ToolDefinition(
        name="file_read",
        description=(
            "Read a file from the workspace directory. Use this to load saved data, "
            "check what was written in a previous step, or inspect existing files."
        ),
        input_schema={
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Relative path inside workspace, e.g. 'notes.txt' or 'data/results.json'.",
                },
            },
            "required": ["path"],
        },
    ),
    execute=_read,
)


# ── Write ──────────────────────────────────────────────────────────────────────

def _write(input: dict) -> str:
    try:
        file_path = _safe_path(input["path"])
    except ValueError as e:
        return f"Error: {e}"

    content = input["content"]
    append = input.get("append", "false").lower() == "true"

    # Make sure parent directories exist
    file_path.parent.mkdir(parents=True, exist_ok=True)

    mode = "a" if append else "w"
    file_path.open(mode, encoding="utf-8").write(content)

    action = "Appended" if append else "Wrote"
    return f'{action} {len(content)} characters to "{input["path"]}".'


file_write_tool = Tool(
    definition=ToolDefinition(
        name="file_write",
        description=(
            "Write content to a file in the workspace directory. Creates the file "
            "if it doesn't exist. Set append='true' to add to an existing file."
        ),
        input_schema={
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Relative path for the file, e.g. 'output/report.txt'.",
                },
                "content": {
                    "type": "string",
                    "description": "The text content to write.",
                },
                "append": {
                    "type": "string",
                    "description": "Set to 'true' to append instead of overwrite. Default 'false'.",
                },
            },
            "required": ["path", "content"],
        },
    ),
    execute=_write,
)


# ── List ───────────────────────────────────────────────────────────────────────

def _list(input: dict) -> str:
    subpath = input.get("path", ".")
    try:
        dir_path = _safe_path(subpath)
    except ValueError as e:
        return f"Error: {e}"

    if not dir_path.exists():
        return f'Directory not found: "{subpath}"'

    entries = sorted(dir_path.iterdir(), key=lambda e: (e.is_file(), e.name))
    if not entries:
        return f'Directory "{subpath}" is empty.'

    lines = [f'  {"/" if e.is_dir() else " "} {e.name}' for e in entries]
    return f'Contents of "{subpath}":\n' + "\n".join(lines)


file_list_tool = Tool(
    definition=ToolDefinition(
        name="file_list",
        description=(
            "List files and directories inside the workspace. Use this before "
            "reading or writing to understand what already exists."
        ),
        input_schema={
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Subdirectory to list. Defaults to the workspace root.",
                },
            },
            "required": [],
        },
    ),
    execute=_list,
)