# src/tools/registry.py
from src.tools.web_search import web_search_tool
from src.tools.file_system import file_read_tool, file_write_tool, file_list_tool
from src.tools.calculator import calculator_tool
from src.types import Tool

# ── Single source of truth ─────────────────────────────────────────────────────
# To add a new tool: build it, import it here, add it to ALL_TOOLS.
# The agent and API call pick it up automatically — nothing else to change.

ALL_TOOLS: list[Tool] = [
    web_search_tool,
    file_read_tool,
    file_write_tool,
    file_list_tool,
    calculator_tool,
]

# O(1) lookup by name for execution
TOOL_MAP: dict[str, Tool] = {t.definition["name"]: t for t in ALL_TOOLS}

# Ready to pass straight into client.messages.create(tools=...)
TOOL_DEFINITIONS = [t.definition for t in ALL_TOOLS]