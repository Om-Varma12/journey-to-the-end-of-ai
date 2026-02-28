from .state import State
from agents import repo_analyzer, code_explainer, router


async def analyze_repo_node(state: State):
    print("repo analyzer came")
    result = await repo_analyzer.run(
        user_query = state['user_question'],
        repo_name = state['repo_name'],
        repo_details = state["repo_details"],
        repoStructure = state['repo_structure']
    )
    return {
        "final_answer": result
    }
    
def explain_code_node(state: State):
    print("Code agent invoked")

async def router_node(state: State):
    result = await router.run(state['user_question'])
    return {
        "next_node": result
    }