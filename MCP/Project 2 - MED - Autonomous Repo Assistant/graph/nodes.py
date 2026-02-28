from .state import State
from agents import repo_analyzer, code_explainer


async def analyze_repo_node(state: State):
    result = await repo_analyzer.run(
        query = state['user_question'],
        username=state["username"],
        repoName=state["repo_name"],
        repoPath = state['repo_path'],
        repoStructure = state['repo_structure']
    )


def explain_code_node(state: State):
    answer = code_explainer.run(
        question=state["user_question"],
        files=state.get("relevant_files", []),
        repo_summary=state.get("repo_summary", ""),
        repo_name=state["repo_name"]
    )

    state["final_answer"] = answer
    return state