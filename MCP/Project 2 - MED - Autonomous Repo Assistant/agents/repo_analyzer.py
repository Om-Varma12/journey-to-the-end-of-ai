import asyncio
from langchain_groq import ChatGroq
from langchain_core.messages import ToolMessage, HumanMessage
from dotenv import load_dotenv
load_dotenv()

llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0)

with open('prompts/analyzer.txt', 'r') as f:
    PROMPT = f.read()

async def _run(question, repo_name, repo_details, repoStructure):
    prompt = (
        PROMPT
        .replace("{user_question}", question)
        .replace("{repo_name}", repo_name)
        .replace("{repo_details}", str(repo_details))
        .replace("{repo_structure}", str(repoStructure))
    )
    reponse = llm.invoke(prompt)
    return reponse.content

async def run(user_query, repo_name, repo_details, repoStructure):
    return await _run(user_query, repo_name, repo_details, repoStructure)

# if __name__ == "__main__":
#     print(asyncio.run(_run("What does this repo do?", "PaperForge", "{'repo_description': 'Ever thought how easy it would be to generate an IEEE research paper from a single idea? PaperForge makes it happen with AI.', 'repo_language': 'Python'}", "{'tree': {'.gitignore': {}, 'BACK': {'main.py': {}, 'services': {'ieeeFormat.py': {}, 'llm.py': {}}, 'tests': {'normalTest.py': {}}, 'utils': {'prompt.py': {}}}, 'FRONT': {'main.py': {}, 'assets': {'styles.css': {}}}}, 'all_files': ['.gitignore', 'BACK/main.py', 'FRONT/main.py', 'FRONT/assets/styles.css', 'BACK/services/ieeeFormat.py', 'BACK/services/llm.py', 'BACK/tests/normalTest.py', 'BACK/utils/prompt.py'], 'by_extension': {'no_extension': ['.gitignore'], '.py': ['BACK/main.py', 'FRONT/main.py', 'BACK/services/ieeeFormat.py', 'BACK/services/llm.py', 'BACK/tests/normalTest.py', 'BACK/utils/prompt.py'], '.css': ['FRONT/assets/styles.css']}, 'important_files': ['BACK/main.py', 'FRONT/main.py']}")))