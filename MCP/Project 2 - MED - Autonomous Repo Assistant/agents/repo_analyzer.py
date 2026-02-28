import asyncio
from langchain_groq import ChatGroq
from langchain_mcp_adapters.client import MultiServerMCPClient
from dotenv import load_dotenv
load_dotenv()

llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0)

client = MultiServerMCPClient({
    "repo": {
        "command": "python",
        "args": ["-u", "mcp_server/server.py"],
        "transport": "stdio",
    }
})

# Cache tools to avoid multiple get_tools() calls that cause freezing
_tools_cache = None

async def _get_tools():
    global _tools_cache
    if _tools_cache is None:
        _tools_cache = await client.get_tools()
    return _tools_cache

async def _run(username: str, repo_name: str):
    prompt = f"""
        You are a GitHub repo analyst.
        Username: {username}
        Repo: {repo_name}

        Decide tool:
        - clone_repo
        - get_repo_information
    """

    tools = await _get_tools()
    model_with_tools = llm.bind_tools(tools)

    response = await model_with_tools.ainvoke(prompt)

    if response.tool_calls:
        tool_call = response.tool_calls[0]
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]

        tool = {t.name: t for t in tools}[tool_name]
        tool_result = await tool.ainvoke(tool_args)

        if isinstance(tool_result, list) and len(tool_result) > 0:
            tool_result = tool_result[0]

        return {
            "tool_name": tool_name,
            "output": tool_result
        }

    return {"tool_name": None, "output": {}}


async def run(username: str, repoName: str):
    return await _run(username, repoName)