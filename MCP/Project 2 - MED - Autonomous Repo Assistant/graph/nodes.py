from .state import State
from agents import (
    router,
    repo_analyzer_router,
    overview_agent,
    arch_agent,
    data_flow_agent,
    file_summarizer_agent, 
    code_explainer,
    file_resolver_agent
)
from services.file_service import read_file_content
import ast


async def router_node(state: State):
    result = await router.run(state["user_question"])
    return {"next_node": result.strip()}


async def repo_analyzer_router_node(state: State):
    print("repo analyzer sub-router invoked")

    result = await repo_analyzer_router.run(state["user_question"])
    return {"sub_next_node": result.strip()}


async def overview_node(state: State):
    print("overview agent invoked")

    result = await overview_agent.run(
        user_query=state["user_question"],
        repo_name=state["repo_name"],
        repo_details=state["repo_details"],
        repo_structure=state["repo_structure"],
    )

    return {"final_answer": result}


async def architecture_node(state: State):
    print("architecture agent invoked")

    result = await arch_agent.run(
        user_query=state["user_question"],
        repo_name=state["repo_name"],
        repo_details=state["repo_details"],
        repo_structure=state["repo_structure"],
    )

    return {"final_answer": result}


async def dataflow_node(state: State):
    print("dataflow agent invoked")

    result = await data_flow_agent.run(
        user_query=state["user_question"],
        repo_name=state["repo_name"],
        repo_details=state["repo_details"],
        repo_structure=state["repo_structure"],
    )

    return {"final_answer": result}


async def explain_code_node(state: State):
    print("code explainer invoked")

    question = state["user_question"]
    repo_name = state["repo_name"]
    repo_structure = state["repo_structure"]

    # initialize cache
    if "file_cache" not in state or state["file_cache"] is None:
        state["file_cache"] = {}

    # initialize current files
    if "current_files" not in state:
        state["current_files"] = None
        
    resolved = await file_resolver_agent.run(
        user_query=question,
        repo_structure=repo_structure,
        current_files=state["current_files"],
    )

    if resolved == "NONE":
        return {"final_answer": "Could not determine which file you are referring to."}

    try:
        resolved_files = ast.literal_eval(resolved)
    except:
        return {"final_answer": "File resolution failed."}

    if not resolved_files:
        return {"final_answer": "No matching files found."}

    state["current_files"] = resolved_files

    explanations = []

    for file_path in resolved_files:

        if file_path not in state["file_cache"]:
            print(f"summarizing {file_path}...")

            content = read_file_content(repo_name, file_path)

            summary = await file_summarizer_agent.run(
                file_name=file_path,
                file_content=content,
            )

            state["file_cache"][file_path] = summary

        file_summary = state["file_cache"][file_path]

        explanation = await code_explainer.run(
            user_query=question,
            file_name=file_path,
            file_summary=file_summary,
        )

        explanations.append(f"### {file_path}\n\n{explanation}")

    final_output = "\n\n".join(explanations)

    return {"final_answer": final_output}