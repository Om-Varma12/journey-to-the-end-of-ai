import json

class Agent:
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = {tool.name: tool for tool in tools}

    def run(self, task):
        print("Agent Started\n")

        # 🧠 Step 1: ask LLM what to do
        response = self.llm.call([
            {
                "role": "system",
                "content": """
                    You are an AI agent.

                    If the user query requires web search, respond ONLY in valid JSON:
                    {"tool": "Web Search", "input": "<query>"}

                    Rules:
                    - Do NOT add any extra text
                    - Do NOT explain
                    - Output ONLY JSON

                    If no tool is needed, respond normally.
                """
            },
            {"role": "user", "content": task}
        ])

        print("LLM Decision:\n", response)

        # 🧪 Step 2: try parsing tool call
        try:
            data = json.loads(response)

            tool_name = data["tool"]
            tool_input = data["input"]

            tool = self.tools.get(tool_name)

            if tool:
                print("\nUsing Tool:", tool_name)
                result = tool.run(tool_input)

                print("\nTool Result:\n", result)

                # 🧠 Step 3: send result back to LLM
                final = self.llm.call([
                    {
                        "role": "system",
                        "content": "You are an AI assistant. Use the tool result to answer the user's question clearly."
                    },
                    {
                        "role": "user",
                        "content": f"User query: {task}\n\nTool result:\n{result}"
                    }
                ])

                print("\nFinal Answer:\n", final)
                return

        except Exception as e:
            print("Parsing failed:", e)

        # fallback (no tool)
        print("\nFinal Answer:\n", response)