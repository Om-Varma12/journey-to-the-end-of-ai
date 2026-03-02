from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()

llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0)

with open("prompts/file_resolver.txt") as f:
    PROMPT = f.read()

async def _run(user_query: str, repo_structure: dict, current_files: list | None):
    prompt = (
        PROMPT
        .replace("{user_query}", user_query)
        .replace("{repo_structure}", str(repo_structure))
        .replace("{current_files}", str(current_files))
    )

    response = await llm.ainvoke(prompt)
    return response.content.strip()

async def run(user_query: str, repo_structure: dict, current_files=None):
    return await _run(user_query, repo_structure, current_files)