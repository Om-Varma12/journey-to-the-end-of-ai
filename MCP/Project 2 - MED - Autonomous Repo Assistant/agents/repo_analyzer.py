import asyncio
from langchain_groq import ChatGroq
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.messages import ToolMessage, HumanMessage
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

with open('prompts/analyzer.txt', 'r') as f:
    PROMPT = f.read()

async def _run(question, username, repo_name, repoStructure: dict | None = None):
    prompt = (
        PROMPT
        .replace("{user_query}", question)
        .replace("{username}", username)
        .replace("{repo_name}", repo_name)
    )
    if(repoStructure != None):
        prompt += "\nRepo Structure: \n" + str(repoStructure)

    tools = await client.get_tools()

    model_with_tools = llm.bind_tools(tools)

    # Use proper message object
    messages = [HumanMessage(content=prompt)]

    while True:
        response = await model_with_tools.ainvoke(messages)
        print(response)
        print()
        print()
        # If no tool calls → final answer
        if not response.tool_calls:
            print(response.content)
            return response.content

        # Append assistant message before executing tools
        messages.append(response)

        # Execute ALL tool calls
        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]

            tool = {t.name: t for t in tools}[tool_name]

            try:
                tool_result = await tool.ainvoke(tool_args)
            except Exception as e:
                raise e

            # Convert result safely to string
            tool_result_str = str(tool_result)

            # Append tool response to conversation
            messages.append(
                ToolMessage(
                    content=tool_result_str,
                    tool_call_id=tool_call["id"]
                )
            )

async def run(user_query, username, repo_name, repoStructure):
    return await _run(user_query, username, repo_name, repoStructure)

# if __name__ == "__main__":
#     print(asyncio.run(_run("What does this repo do?", "Om-Varma12", "PaperForge")))