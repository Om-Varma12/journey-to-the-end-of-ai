import asyncio
from langchain_groq import ChatGroq
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv

load_dotenv()

async def main():

    llm = ChatGroq(model="openai/gpt-oss-20b")

    # MCP connection
    mcp_client = MultiServerMCPClient({
        "FileSystem": {
            "command": "python",
            "args": ["./server.py"],
            "transport": "stdio"
        }
    })

    tools = await mcp_client.get_tools()

    # memory
    memory = MemorySaver()

    agent = create_agent(
        model=llm,
        tools=tools,
        checkpointer=memory
    )

    thread_id = "user-1"

    while True:
        user_input = input("You: ")

        result = await agent.ainvoke(
            {"messages": [("user", user_input)]},
            config={"configurable": {"thread_id": thread_id}}
        )

        print("AI:", result["messages"][-1].content)

asyncio.run(main())