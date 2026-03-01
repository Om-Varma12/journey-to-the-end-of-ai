from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()

llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0)

with open("prompts/code_explainer.txt") as f:
    PROMPT = f.read()

async def _run(user_query: str, file_name: str, file_summary: str):
    prompt = (
        PROMPT
        .replace("{user_query}", user_query)
        .replace("{file_name}", file_name)
        .replace("{file_summary}", file_summary)
    )

    response = await llm.ainvoke(prompt)
    return response.content

async def run(user_query: str, file_name: str, file_summary: str):
    return await _run(user_query, file_name, file_summary)