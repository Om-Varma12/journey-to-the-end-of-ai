from state import State
from agents import repo_analyzer
from agents import code_explainer

def analyze_repo_node(state: State):
    summary = repo_analyzer.run(state["repo_path"])
    state["repo_summary"] = summary
    return state


# def search_files_node(state: State):
#     files = search_tool.run(state["repo_path"], state["user_question"])
#     state["relevant_files"] = files
#     return state


def explain_code_node(state: State):
    answer = code_explainer.run(
        question=state["user_question"],
        files=state["relevant_files"],
        repo_summary=state["repo_summary"]
    )
    state["final_answer"] = answer
    return state