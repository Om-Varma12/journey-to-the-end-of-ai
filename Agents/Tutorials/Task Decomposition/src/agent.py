import json
import re
from prompts.agent import SYSTEM_PROMPT, USER_PROMPT
from tools.web_search import WebSearchTool


class Agent:
    def __init__(self, llm):
        self.llm = llm
        self.web_search = WebSearchTool()

    def execute(self, context, taskDescription):
        prompt = (
            USER_PROMPT
            .replace('{previous_results}', context)
            .replace('{current_task}', taskDescription)
        )
        
        while True:
            response = self.llm.generate(SYSTEM_PROMPT, prompt)
            data = json.loads(response)

            if data["action"] == "answer":
                return data["final_answer"]

            elif data["action"] == "web_search":
                result = self.web_search.run(data["query"])

                tool_output = {
                    "tool": "web_search",
                    "query": data["query"],
                    "results": result
                }

                prompt += "\nTool Output:\n" + json.dumps(tool_output, indent=2)
            

# from .llm import LLM
# llm = LLM()
# agent = Agent(llm)
# agent.execute('', 'latest news on ai')