from state import State
from agents import repo_analyzer
from agents import code_explainer

def analyze_repo_node(state: State):
    result = repo_analyzer.run(
        username=state["username"],
        repoName=state["repo_name"]
    )

    tool_used = result.get("tool_name")
    output = result.get("output", {})

    if tool_used == "clone_repo":
        state["repo_path"] = output.get("repo_path")
        state["repo_structure"] = output.get("repo_structure")

    elif tool_used == "get_repo_information":
        state["repo_description"] = output.get("description")
        state["repo_language"] = output.get("language")
        state["repo_created_at"] = output.get("created_at")
        state["repo_updated_at"] = output.get("lasted_updated_at")

    return state


# def search_files_node(state: State):
#     files = search_tool.run(state["repo_path"], state["user_question"])
#     state["relevant_files"] = files
#     return state


def explain_code_node(state: State):
    answer = code_explainer.run(
        question = state["user_question"],
        files = state["relevant_files"],
        repo_summary = state["repo_summary"],
        repo_name = state['repo_name']
    )
    state["final_answer"] = answer
    return state