from .state import State
from agents import repo_analyzer, code_explainer


async def analyze_repo_node(state: State):
    result = await repo_analyzer.run(
        username=state["username"],
        repoName=state["repo_name"]
    )

    tool_used = result.get("tool_name")
    output = result.get("output") or {}

    # normalize MCP output
    if isinstance(output, list):
        output = output[0] if output else {}

    if tool_used == "clone_repo":
        state["repo_path"] = output.get("repo_path")
        state["repo_structure"] = output.get("repo_structure")
        state["final_answer"] = "Repo cloned."

    elif tool_used == "get_repo_information":
        state["repo_description"] = output.get("description")
        state["repo_language"] = output.get("language")
        state["repo_summary"] = output.get("description")
        state["final_answer"] = state["repo_description"]

    return state


def explain_code_node(state: State):
    answer = code_explainer.run(
        question=state["user_question"],
        files=state.get("relevant_files", []),
        repo_summary=state.get("repo_summary", ""),
        repo_name=state["repo_name"]
    )

    state["final_answer"] = answer
    return state