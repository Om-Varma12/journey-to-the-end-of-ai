from langchain_groq import ChatGroq
from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio
from dotenv import load_dotenv
load_dotenv()

llm = ChatGroq(model = "openai/gpt-oss-20b", temperature=0)

client = MultiServerMCPClient({
    "repo": {
        "command": "python",
        "args": ["mcp_server/server.py"],
        "transport": "stdio",
    }
})

async def run(username: str, repo_name: str):
    prompt = f"""
        You are a senior GitHub repository analyst.

        Username: {username}
        Repository: {repo_name}
    """

    tools = await client.get_tools()
    model_with_tools = llm.bind_tools(tools)

    response = await model_with_tools.ainvoke(prompt)

    print("\nMODEL RESPONSE:")
    print(response)

    if response.tool_calls:
        tool_call = response.tool_calls[0]
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]

        print("\nTOOL CHOSEN:", tool_name)
        print("ARGS:", tool_args)

        tool = {t.name: t for t in tools}[tool_name]

        tool_result = await tool.ainvoke(tool_args)

        print("\n=== TOOL OUTPUT ===")
        print(tool_result)

    else:
        print("\nNO TOOL CALLED")    
        
        
asyncio.run(run("Om-Varma12", "CrackEM"))