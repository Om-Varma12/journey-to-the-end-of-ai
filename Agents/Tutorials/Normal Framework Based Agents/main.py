from config import MODEL
from llm import LLM
from agent import Agent
from web_search import TavilySearchTool

llm = LLM(MODEL)
tavily_tool = TavilySearchTool()

agent = Agent(llm=llm, tools=[tavily_tool])

query = input("Enter your query: ")
agent.run(query)