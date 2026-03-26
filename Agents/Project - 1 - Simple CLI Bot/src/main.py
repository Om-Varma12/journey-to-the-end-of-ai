# src/main.py
import os
import sys
from dotenv import load_dotenv
from src.agent import Agent
from src.types import AgentConfig

load_dotenv()


SYSTEM_PROMPT = """You are a helpful personal assistant running in a terminal.

You have access to these tools:
- web_search: find current information online
- file_read: read files from the workspace directory
- file_write: write or append files to the workspace directory  
- file_list: list files inside the workspace directory
- calculator: evaluate any mathematical expression precisely

Guidelines:
- Think before acting. If a task needs multiple steps, work through them one at a time.
- Always use the calculator tool for arithmetic — never compute in your head.
- When you write a file, confirm the path and character count.
- If a tool returns an error, explain what went wrong and try an alternative if possible.
- Be concise but thorough. Don't pad your responses.
- If you're uncertain about a fact, say so and use web_search to verify.

The workspace directory is where all files live. You can organise it however you like."""


config = AgentConfig(
    model="openai/gpt-oss-120b",
    max_tokens=8192,
    max_iterations=15,
    system_prompt=SYSTEM_PROMPT,
)

agent = Agent(config)

# ── ANSI colours ───────────────────────────────────────────────────────────────
RESET  = "\x1b[0m"
BOLD   = "\x1b[1m"
DIM    = "\x1b[2m"
CYAN   = "\x1b[36m"
GREEN  = "\x1b[32m"
YELLOW = "\x1b[33m"


def print_banner():
    print(f"""
{BOLD}{CYAN}╭──────────────────────────────────────╮
│   P1 — CLI Personal Assistant        │
│   Commands: exit · reset · history   │
╰──────────────────────────────────────╯{RESET}
""")


def main():
    print_banner()

    while True:
        try:
            user_input = input(f"{BOLD}{GREEN}You: {RESET}").strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n{DIM}Goodbye!{RESET}")
            sys.exit(0)

        if not user_input:
            continue

        # ── Built-in commands ──────────────────────────────────────────────────
        if user_input.lower() == "exit":
            print(f"\n{DIM}Goodbye!{RESET}")
            sys.exit(0)

        if user_input.lower() == "reset":
            agent.reset()
            print(f"{DIM}Conversation cleared.{RESET}\n")
            continue

        if user_input.lower() == "history":
            history = agent.get_history()
            print(f"\n{DIM}=== {len(history)} messages in history ==={RESET}")
            for i, msg in enumerate(history):
                content = msg["content"]
                if isinstance(content, str):
                    preview = content[:80]
                elif isinstance(content, list):
                    preview = f"[{len(content)} blocks]"
                else:
                    preview = str(content)[:80]
                print(f"  {DIM}[{i}] {msg['role']}: {preview}{RESET}")
            print()
            continue

        # ── Send to agent ──────────────────────────────────────────────────────
        print(f"\n{BOLD}{YELLOW}Assistant:{RESET} ", end="", flush=True)

        try:
            agent.chat_stream(user_input)
        except Exception as e:
            print(f"\n{DIM}[Error] {e}{RESET}")

        print("\n")


if __name__ == "__main__":
    main()