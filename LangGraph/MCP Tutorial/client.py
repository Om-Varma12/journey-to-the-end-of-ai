import asyncio
from dotenv import load_dotenv

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain_groq import ChatGroq

load_dotenv()


async def main():
    client = MultiServerMCPClient(
        {
            "add": {
                "command": "python",
                "args": ["./add_server.py"], 
                "transport": "stdio",
            },
            "multiply": {
                "command": "python",
                "args": ["./mult_server.py"], 
                "transport": "stdio",
            },
            "weather": {
                "url": "http://127.0.0.1:8000/mcp",
                "transport": "streamable_http",
            },
        }
    )

    tools = await client.get_tools()

    model = ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0
    )

    agent = create_agent(
        model=model,
        tools=tools
    )

    result = await agent.ainvoke(
        {"messages": [("user", "what is 6 + 7. And then multiply the result by 7. Give me step by step answer")]}
    )

    print(result['messages'][-1].content)


if __name__ == "__main__":
    asyncio.run(main())