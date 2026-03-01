from .state import State
from agents import (
    router,
    repo_analyzer_router,
    overview_agent,
    arch_agent,
    data_flow_agent,
    code_explainer
)


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

    result = await code_explainer.run(
        user_query=state["user_question"],
        repo_name=state["repo_name"],
        repo_structure=state["repo_structure"],
    )

    return {"final_answer": result}