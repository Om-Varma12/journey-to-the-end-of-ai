from langchain_groq import ChatGroq
import asyncio
from dotenv import load_dotenv
load_dotenv()

llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0)
with open('prompts/router.txt') as f:
    PROMPT = f.read()

async def _run(user_query: str):
    prompt = PROMPT.replace('{user_query}', user_query)
    response = await llm.ainvoke(prompt)
    return response.content

# async def run(user_query):
#     return await _run(user_query)

if __name__ == "__main__":
    print(asyncio.run(_run("What does this repo do?")))