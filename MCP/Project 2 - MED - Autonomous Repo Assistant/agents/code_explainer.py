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


async def _run(question, files, repo_summary, repo_name):
    prompt = f"""
        Explain code shortly.

        Question: {question}
        Files: {files}
        Repo Summary: {repo_summary}
        Repo Name: {repo_name}
    """

    tools = await client.get_tools()
    model_with_tools = llm.bind_tools(tools)

    response = await model_with_tools.ainvoke(prompt)

    if response.tool_calls:
        tool_call = response.tool_calls[0]
        tool = {t.name: t for t in tools}[tool_call["name"]]
        tool_result = await tool.ainvoke(tool_call["args"])

        final = await model_with_tools.ainvoke([
            response,
            {
                "role": "tool",
                "tool_call_id": tool_call["id"],
                "content": tool_result
            }
        ])
        return final.content

    return response.content


async def run(question, files, repo_summary, repo_name):
    return await _run(question, files, repo_summary, repo_name)