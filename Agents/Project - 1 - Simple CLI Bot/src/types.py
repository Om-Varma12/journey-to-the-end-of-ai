# src/types.py
from typing import Any, TypedDict, Callable
from dataclasses import dataclass, field


# ── What you send to Anthropic to describe a tool ──────────────────────────────
class ToolInputProperty(TypedDict, total=False):
    type: str
    description: str
    enum: list[str]


class ToolInputSchema(TypedDict):
    type: str                                    # always "object"
    properties: dict[str, ToolInputProperty]
    required: list[str]


class ToolDefinition(TypedDict):
    name: str
    description: str
    input_schema: ToolInputSchema


# ── Chat messages ─────────────────────────────────────────────────────────────
class Message(TypedDict):
    role: str
    content: Any


# Convenience alias for code that imports the plural form.
Messages = list[Message]


# ── What you send BACK after running a tool ─────────────────────────────────────
class ToolResult(TypedDict, total=False):
    type: str           # always "tool_result"
    tool_use_id: str    # must match the id Claude gave you — the API enforces this
    content: str        # always a string; json.dumps() complex objects
    is_error: bool      # optional — set True if the tool failed


# ── A tool: its API definition + the function that runs it ──────────────────────
@dataclass
class Tool:
    definition: ToolDefinition
    execute: Callable[[dict[str, Any]], str]
    # Note: execute is synchronous — we keep it simple for P1.
    # In P4+ you'll make this async for concurrent tool execution.


# ── Agent configuration ─────────────────────────────────────────────────────────
@dataclass
class AgentConfig:
    model: str = "openai/gpt-oss-120b"
    max_tokens: int = 8192
    max_iterations: int = 15    # safety cap — stops runaway loops
    system_prompt: str = ""