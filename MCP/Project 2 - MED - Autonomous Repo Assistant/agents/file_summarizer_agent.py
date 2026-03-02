from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()

llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0)

with open("prompts/file_summary.txt") as f:
    PROMPT = f.read()

async def _run(file_name: str, file_content: str):
    prompt = (
        PROMPT
        .replace("{file_name}", file_name)
        .replace("{file_content}", file_content)
    )

    response = await llm.ainvoke(prompt)
    return response.content

async def run(file_name: str, file_content: str):
    return await _run(file_name, file_content)