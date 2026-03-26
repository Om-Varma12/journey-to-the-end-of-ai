import time
import sys
import json
from groq import Groq

from .types import AgentConfig, Message, ToolResult
from .tools.registry import TOOL_DEFINITIONS, TOOL_MAP


# ── Retry logic ───────────────────────────────────────────

def _with_retry(fn, max_attempts: int = 4, base_delay: float = 1.0):
    for attempt in range(max_attempts):
        try:
            return fn()
        except Exception as e:
            if attempt == max_attempts - 1:
                raise
            delay = base_delay * (2 ** attempt)
            print(f"\n  [agent] error — retrying in {delay:.0f}s", file=sys.stderr)
            time.sleep(delay)


# ── Tool executor ─────────────────────────────────────────

def _execute_tool(tool_name: str, tool_input: dict):
    tool = TOOL_MAP.get(tool_name)

    if tool is None:
        return f'Unknown tool "{tool_name}"'

    try:
        return tool.execute(tool_input)
    except Exception as e:
        return f"Tool error: {e}"


# ── Agent ────────────────────────────────────────────────

class Agent:
    def __init__(self, config: AgentConfig):
        self.config = config
        self.client = Groq()
        self.history: list[Message] = []

    def reset(self):
        self.history = []

    def get_history(self):
        return list(self.history)

    def chat(self, user_message: str) -> str:
        self.history.append({"role": "user", "content": user_message})

        iterations = 0

        while iterations < self.config.max_iterations:
            iterations += 1
            print(f"\n  [agent] iteration {iterations}", file=sys.stderr)

            response = _with_retry(lambda: self.client.chat.completions.create(
                model=self.config.model,
                messages=self.history,
                tools=TOOL_DEFINITIONS,
                tool_choice="auto",
                temperature=0.7,
            ))

            message = response.choices[0].message

            # ✅ Handle native tool calling
            if hasattr(message, 'tool_calls') and message.tool_calls:
                # Append assistant message with tool calls
                self.history.append({
                    "role": "assistant",
                    "content": message.content or "",
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments,
                            }
                        }
                        for tc in message.tool_calls
                    ]
                })

                # Execute each tool and collect results
                tool_results = []
                for tool_call in message.tool_calls:
                    tool_name = tool_call.function.name
                    try:
                        tool_input = json.loads(tool_call.function.arguments)
                    except json.JSONDecodeError:
                        tool_input = {}

                    result = _execute_tool(tool_name, tool_input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": tool_call.id,
                        "content": result,
                    })

                # Add tool results as user message
                self.history.append({
                    "role": "user",
                    "content": tool_results,
                })

                continue

            # ✅ Normal response
            self.history.append({
                "role": "assistant",
                "content": message.content
            })

            return message.content

        return "[Max iterations reached]"

    def chat_stream(self, user_message: str) -> None:
        self.history.append({"role": "user", "content": user_message})

        iterations = 0

        while iterations < self.config.max_iterations:
            iterations += 1
            print(f"\n  [agent] iteration {iterations}", file=sys.stderr)

            response = _with_retry(lambda: self.client.chat.completions.create(
                model=self.config.model,
                messages=self.history,
                tools=TOOL_DEFINITIONS,
                tool_choice="auto",
                temperature=0.7,
            ))

            message = response.choices[0].message

            # ✅ Handle native tool calling
            if hasattr(message, 'tool_calls') and message.tool_calls:
                # Append assistant message with tool calls
                self.history.append({
                    "role": "assistant",
                    "content": message.content or "",
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments,
                            }
                        }
                        for tc in message.tool_calls
                    ]
                })

                # Execute each tool and collect results
                tool_results = []
                for tool_call in message.tool_calls:
                    tool_name = tool_call.function.name
                    try:
                        tool_input = json.loads(tool_call.function.arguments)
                    except json.JSONDecodeError:
                        tool_input = {}

                    result = _execute_tool(tool_name, tool_input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": tool_call.id,
                        "content": result,
                    })

                # Add tool results as user message
                self.history.append({
                    "role": "user",
                    "content": tool_results,
                })

                continue

            # ✅ Normal response
            self.history.append({
                "role": "assistant",
                "content": message.content
            })

            print(message.content, end="", flush=True)
            return

        print("[Max iterations reached]")