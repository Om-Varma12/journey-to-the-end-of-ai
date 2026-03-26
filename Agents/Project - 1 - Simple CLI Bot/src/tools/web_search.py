# src/tools/web_search.py
import os
import requests
from src.types import Tool, ToolDefinition


def _execute(input: dict) -> str:
    query = input["query"]
    count = min(int(input.get("num_results", 5)), 10)
    api_key = os.getenv("TAVILY_API_KEY")

    # ── Graceful degradation ────────────────────────────────────────────────
    if not api_key:
        return (
            f'[Mock result — set TAVILY_API_KEY for real search]\n'
            f'Query was: "{query}"\n'
            f'This is placeholder data.'
        )

    try:
        response = requests.post(
            "https://api.tavily.com/search",
            json={
                "api_key": api_key,
                "query": query,
                "search_depth": "basic",  # or "advanced"
                "max_results": count,
            },
            timeout=10,
        )
    except Exception as e:
        return f"Search request failed: {str(e)}"

    # ── Return errors as strings, never raise ───────────────────────────────
    if not response.ok:
        return f"Search API error: {response.status_code} {response.reason}"

    data = response.json()
    results = data.get("results", [])

    if not results:
        return "No results found."

    # ── Format results cleanly for LLM ──────────────────────────────────────
    return "\n\n".join(
        f"[{i+1}] {r.get('title', 'No title')}\n"
        f"    {r.get('url', 'No URL')}\n"
        f"    {r.get('content', 'No description')}"
        for i, r in enumerate(results)
    )


web_search_tool = Tool(
    definition=ToolDefinition(
        name="web_search",
        description=(
            "Search the web for current information. Use this when the user asks "
            "about recent events, current prices, live data, or anything that may "
            "have changed since your training cutoff. Returns titles, URLs and snippets."
        ),
        input_schema={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query. Specific queries work better — aim for 3-8 words.",
                },
                "num_results": {
                    "type": "string",
                    "description": "How many results to return (1-10). Default is 5.",
                },
            },
            "required": ["query"],
        },
    ),
    execute=_execute,
)