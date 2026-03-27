import json
import re
from prompts.decomposer import SYSTEM_PROMPT, USER_PROMPT
from .task import Task


class DecomposerAgent:
    def __init__(self, llm):
        self.llm = llm

    def _safe_parse(self, text):
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            return json.loads(match.group())
        raise ValueError("Invalid JSON from LLM")

    def _convert_to_tasks(self, data: dict):
        tasks = []

        for task_key, task_value in data.items():
            task_id = int(task_key.replace("Task", ""))

            dependedOn = [
                int(t.replace("Task", ""))
                for t in task_value["depends_on"]
            ]

            task = Task(
                id=task_id,
                description=task_value["description"],
                dependedOn=dependedOn
            )

            tasks.append(task)

        return tasks

    def decompose(self, query):
        full_prompt = USER_PROMPT.replace("{input_query}", query)
        response = self.llm.generate(SYSTEM_PROMPT, full_prompt)

        print(response)

        data = self._safe_parse(response)
        tasks = self._convert_to_tasks(data)

        return tasks