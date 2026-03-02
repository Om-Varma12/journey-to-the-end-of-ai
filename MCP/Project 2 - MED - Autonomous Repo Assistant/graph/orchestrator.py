from langgraph.graph import StateGraph, END
from .state import State
from .nodes import (
    router_node,
    repo_analyzer_router_node,
    overview_node,
    architecture_node,
    dataflow_node,
    explain_code_node,
)
from services.repo_service import (
    check_repo_exist,
    clone_repo,
    pull_latest_changes,
    get_repo_details,
    get_repo_structure,
)
import asyncio


graph = StateGraph(State)

# Main level
graph.add_node("router", router_node)
graph.add_node("repo_analyzer_router", repo_analyzer_router_node)
graph.add_node("explain_code", explain_code_node)

# Sub agents
graph.add_node("overview", overview_node)
graph.add_node("architecture", architecture_node)
graph.add_node("dataflow", dataflow_node)

graph.set_entry_point("router")

# MAIN ROUTING
graph.add_conditional_edges(
    "router",
    lambda state: state["next_node"],
    {
        "analyze_repo": "repo_analyzer_router",
        "explain_code": "explain_code",
    }
)

# SUB ROUTING
graph.add_conditional_edges(
    "repo_analyzer_router",
    lambda state: state["sub_next_node"],
    {
        "overview": "overview",
        "architecture": "architecture",
        "dataflow": "dataflow",
    }
)

# END
graph.add_edge("overview", END)
graph.add_edge("architecture", END)
graph.add_edge("dataflow", END)
graph.add_edge("explain_code", END)

app = graph.compile()


async def main():
    state: State = {}

    state["username"] = input("GitHub username: ")
    state["repo_name"] = input("Repo name: ")

    print("Checking if repo exists?...")
    if(check_repo_exist(state['repo_name'])):
        print("Repo exists.")
        print("Pulling latest changes...")
        pull_latest_changes(state['repo_name'])
    else:
        print("Repo not found.")
        print("Cloning the repo...")
        clone_repo(state['username'], state['repo_name'])
        
    state['repo_details'] = get_repo_details(state['username'], state['repo_name'])
    state['repo_structure'] = get_repo_structure(state['repo_name'])
    print("---ALL THINGS SET---")

    while True:
        q = input("\nAsk: ")
        state["user_question"] = q

        result = await app.ainvoke(state)

        print("\nAI:", result.get("final_answer"))

if __name__ == "__main__":
    asyncio.run(main())