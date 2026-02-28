from langgraph.graph import StateGraph, END
from .state import State
from .nodes import analyze_repo_node, explain_code_node
from langchain_groq import ChatGroq
import asyncio

llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0)


# -------- ROUTER --------
def router_node(state: State):
    # first time → must clone
    if not state.get("repo_path"):
        state["next_node"] = "analyze_repo"
        return state

    # if repo cloned but no description yet
    if not state.get("repo_summary"):
        state["next_node"] = "analyze_repo"
        return state

    # ask LLM where to go
    decision = llm.invoke(f"""
User question: {state["user_question"]}

Choose node:
- analyze_repo
- explain_code

Reply only node name.
""")

    state["next_node"] = decision.content.strip()
    return state


# -------- GRAPH --------
graph = StateGraph(State)

graph.add_node("router", router_node)
graph.add_node("analyze_repo", analyze_repo_node)
graph.add_node("explain_code", explain_code_node)

graph.set_entry_point("router")

graph.add_conditional_edges(
    "router",
    lambda state: state["next_node"],
    {
        "analyze_repo": "analyze_repo",
        "explain_code": "explain_code",
    }
)

# after analyze → go back to router
graph.add_edge("analyze_repo", "router")
graph.add_edge("explain_code", END)

app = graph.compile()


async def main():
    state: State = {}

    state["username"] = input("GitHub username: ")
    state["repo_name"] = input("Repo name: ")

    while True:
        q = input("\nAsk: ")
        state["user_question"] = q

        result = await app.ainvoke(state)

        print("\nAI:", result.get("final_answer"))

if __name__ == "__main__":
    asyncio.run(main())