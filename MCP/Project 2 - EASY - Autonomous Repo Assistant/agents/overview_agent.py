from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()

llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0)

with open("prompts/overview_agent.txt") as f:
    PROMPT = f.read()

async def _run(user_query, repo_name, repo_details, repo_structure):
    prompt = (
        PROMPT
        .replace("{user_query}", user_query)
        .replace("{repo_name}", repo_name)
        .replace("{repo_details}", str(repo_details))
        .replace("{repo_structure}", str(repo_structure))
    )
    response = await llm.ainvoke(prompt)
    return response.content

async def run(user_query, repo_name, repo_details, repo_structure):
    return await _run(user_query, repo_name, repo_details, repo_structure)