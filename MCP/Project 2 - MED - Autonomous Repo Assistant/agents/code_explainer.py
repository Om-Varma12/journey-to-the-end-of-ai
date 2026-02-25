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


async def run(question, file_path, repo_summary):
    prompt = f"""
        You are a senior level code explainer who has only one task that it to retrieve the file from tool and 
        properly explain what the code does without consuming too much tokens and keeping the explaination
        clean and short.
        Question: {question}
        File_Path: {file_path}
        Complete Repository Summary: {repo_summary}
        
        Give shortest explaination of what the file does.
        Remove all kinds of formating, just returning everything in text format.
    """

    tools = await client.get_tools()
    
    print("Got tools")
    
    model_with_tools = llm.bind_tools(tools)
    print("connected")
    
    response = await model_with_tools.ainvoke(prompt)
    
    # If model requested tool
    if response.tool_calls:
        tool_call = response.tool_calls[0]
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]

        # execute tool
        tool = {t.name: t for t in tools}[tool_name]
        tool_result = await tool.ainvoke(tool_args)

        # send tool result back to model
        final_response = await model_with_tools.ainvoke([
            response,
            {
                "role": "tool",
                "tool_call_id": tool_call["id"],
                "content": tool_result
            }
        ])

        print(final_response.content)
    else:
        print(response.content)
        
    print("retrieved")
    print("DONE")
    
asyncio.run(run("What does followupAgent.py file does?", "ai/agents/followupAgent.py", "This is an AI powered interview taking system named as CrackEM."))