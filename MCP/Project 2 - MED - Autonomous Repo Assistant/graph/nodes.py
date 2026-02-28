from .state import State
from agents import repo_analyzer, code_explainer, router


async def analyze_repo_node(state: State):
    print("repo analyzer came")
    result = await repo_analyzer.run(
        user_query = state['user_question'],
        username = state["username"],
        repo_name = state["repo_name"],
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

async def router_node(state: State):
    result = await router.run(state['user_question'])
    return {
        "next_node": result
    }