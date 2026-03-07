from typing_extensions import TypedDict
from typing import Annotated

from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_core.messages import ToolMessage
from langchain_core.tools import InjectedToolCallId
from langgraph.prebuilt import InjectedState
from langgraph.types import Command


class SubAgent(TypedDict):
    name: str
    description: str
    prompt: str
    tools: list


def create_subagent_tool(subagents, model, state_schema):
    agents = {}

    for agent in subagents:
        agents[agent["name"]] = create_agent(
            model=model,
            system_prompt=agent["prompt"],
            tools=agent["tools"],
            state_schema=state_schema,
        )

    @tool
    def run_subagent(
        description: str,
        agent_name: str,
        state: Annotated[dict, InjectedState],
        tool_call_id: Annotated[str, InjectedToolCallId],
    ):
        """
        Run a specialized subagent with isolated context.
        """

        if agent_name not in agents:
            return f"Agent {agent_name} does not exist"

        subagent = agents[agent_name]

        state["messages"] = [{"role": "user", "content": description}]

        result = subagent.invoke(state)

        return Command(
            update={
                "messages": [
                    ToolMessage(
                        result["messages"][-1].content,
                        tool_call_id=tool_call_id,
                    )
                ]
            }
        )

    return run_subagent