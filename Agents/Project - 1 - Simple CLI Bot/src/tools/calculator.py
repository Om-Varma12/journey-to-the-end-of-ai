# src/tools/calculator.py
import re
import math
from src.types import Tool, ToolDefinition


# ── Why not eval()? ────────────────────────────────────────────────────────────
# eval("__import__('os').system('rm -rf /')") works perfectly.
# We use a whitelist approach instead: only allow the characters
# and names that could appear in a legitimate math expression.
# You'll build proper sandboxed code execution (subprocess + timeout) in P3.

_ALLOWED_NAMES = {
    "abs": abs, "round": round, "min": min, "max": max,
    "sqrt": math.sqrt, "pow": math.pow, "log": math.log,
    "log2": math.log2, "log10": math.log10,
    "sin": math.sin, "cos": math.cos, "tan": math.tan,
    "ceil": math.ceil, "floor": math.floor,
    "pi": math.pi, "e": math.e,
}

# Only these characters can appear in an expression (after stripping function names)
_SAFE_CHARS = re.compile(r'^[\d\s\+\-\*\/\%\(\)\.\,\*\*]+$')


def _execute(input: dict) -> str:
    expr = input["expression"].strip()

    # Step 1: strip known-safe function names so the remaining chars can be validated
    stripped = expr
    for name in _ALLOWED_NAMES:
        stripped = stripped.replace(name, "")

    # Step 2: validate what's left
    if not _SAFE_CHARS.match(stripped):
        return (
            f'Error: expression contains disallowed characters.\n'
            f'Allowed: numbers, +  -  *  /  **  %  ()  and math functions like sqrt(), log(), pi.'
        )

    try:
        # compile() + eval() with a restricted namespace — no builtins, no globals
        result = eval(
            compile(expr, "<string>", "eval"),
            {"__builtins__": {}},   # block ALL builtins
            _ALLOWED_NAMES,         # only our whitelist is in scope
        )

        if not isinstance(result, (int, float)):
            return "Error: expression did not produce a number."

        if result != result:        # NaN check
            return f"{expr} = NaN (not a number)"

        if result == float("inf") or result == float("-inf"):
            return f"{expr} = {'Infinity' if result > 0 else '-Infinity'}"

        # Clean formatting: integers stay as integers, floats drop trailing zeros
        formatted = str(int(result)) if isinstance(result, float) and result.is_integer() else f"{result:.10g}"
        return f"{expr} = {formatted}"

    except ZeroDivisionError:
        return f"Error: division by zero in '{expr}'."
    except Exception as e:
        return f"Error evaluating '{expr}': {e}"


calculator_tool = Tool(
    definition=ToolDefinition(
        name="calculator",
        description=(
            "Evaluate a mathematical expression and return the exact result. "
            "Use this for ANY arithmetic — never compute in your head. "
            "Supports +, -, *, /, **, % and functions like sqrt(), log(), sin(), pi, e."
        ),
        input_schema={
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": (
                        "A math expression. Examples: '2 + 2', 'sqrt(144)', "
                        "'(1000 * 1.07) ** 10', 'log(100, 10)'."
                    ),
                },
            },
            "required": ["expression"],
        },
    ),
    execute=_execute,
)