from langchain_groq import ChatGroq
from . import file_summarizer_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.messages import ToolMessage
import asyncio
from dotenv import load_dotenv
load_dotenv()

llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0)

mcp_client = MultiServerMCPClient(
    {
        "file-server": {
            "command": "python",
            "args": ["mcp_server/server.py"],
            "transport": "stdio",
        }
    }
)


with open("prompts/code_explainer.txt") as f:
    PROMPT = f.read()


async def _run(current_file: str | None, file_cache, user_query: str, repo_name: str, repo_structure):
    tools = await mcp_client.get_tools()
    llm_with_tools = llm.bind_tools(tools)

    prompt = (
        PROMPT
        .replace("{repo_name}", repo_name)
        .replace("{current_file}", str(current_file))
        .replace("{cached_files}", str(file_cache))
        .replace("{user_query}", user_query)
        .replace("{repo_structure}", str(repo_structure))
    )

    response = await llm_with_tools.ainvoke(prompt)

    # -------------------------
    # If LLM calls get_file tool
    # -------------------------
    if response.tool_calls:

        tool_call = response.tool_calls[0]
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]

        # Find matching tool
        tool = {t.name: t for t in tools}[tool_name]

        # Execute tool
        tool_result = await tool.ainvoke(tool_args)

        file_content = tool_result
        resolved_file = tool_args["file_path"]

        # Summarize externally
        file_summary = await file_summarizer_agent.run(
            file_name=resolved_file,
            file_content=file_content
        )

        file_cache[resolved_file] = file_summary
        current_file = resolved_file

        # Final explanation
        final_prompt = f"""
            User Question: {user_query}
            File Name: {resolved_file}
            File Summary: {file_summary}
            Explain clearly and technically.
            """

        final_response = await llm.ainvoke(final_prompt)

        return {
            "response": final_response.content,
            "current_file": current_file,
            "file_cache": file_cache
        }

    # -------------------------
    # If no tool call → must use cache
    # -------------------------
    else:

        # LLM should have inferred file from question or current_file
        # We re-resolve it via second pass for safety

        final_response = response.content

        return {
            "response": final_response,
            "current_file": current_file,
            "file_cache": file_cache
        }
        
        
# if __name__ == "__main__":
#     print(asyncio.run(_run("FRONT/main.py", 
#                            {'FRONT/main.py': 'This file is the Streamlit frontend for PaperForge, a web app that generates IEEE-formatted research papers using a FastAPI backend.🔹 What It Does Sets up UI Page title & icon. Text area for project overview. Select box for format (IEEE). Slider to choose number of pages. Sidebar test button to download an existing output.docx. Handles Paper Generation On clicking “⚡ Forge Research Paper”: Validates input (minimum 30 characters). Sends a POST request to the backend (/generate-docs-stream). Uses Server-Sent Events (SSE) to stream progress updates. Shows Live Progress Displays step-by-step status: 🔍 Validation 🧠 Prompt generation 🤖 LLM response 📄 Document generation Updates each stage dynamically with success/error states. Downloads Final Paper If backend returns success: Reads generated .docx from back/ folder. Displays a download button for the research paper.'}, 
#                            "ok, and what functions does it have?",
#                            "PaperForge"
#     )))
    
async def run(current_file, file_cache, question, repo_name, repo_structure):
    return await _run(current_file, file_cache, question, repo_name, repo_structure)