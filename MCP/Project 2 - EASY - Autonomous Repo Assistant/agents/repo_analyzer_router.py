from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()

llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0)

with open("prompts/repo_analyzer_router.txt") as f:
    PROMPT = f.read()

async def _run(user_query: str):
    prompt = PROMPT.replace("{user_query}", user_query)
    response = await llm.ainvoke(prompt)
    return response.content.strip()

async def run(user_query: str):
    return await _run(user_query)