from src.decomposer import DecomposerAgent
from src.agent import Agent
from src.llm import LLM

llm = LLM()

query = input("Enter your query: ")

print("[decomposer] started")
decomposer = DecomposerAgent(llm)
tasks = decomposer.decompose(query)
print("[decomposer] ended")

# Ensure correct order
tasks = sorted(tasks, key=lambda t: t.id)

task_results = {}
global_context = ""

agent = Agent(llm)

for task in tasks:
    print(f"\n[task {task.id}] {task.description}\n")

    context = ""

    # Dependency context
    if task.dependedOn:
        for dep_id in task.dependedOn:
            if dep_id not in task_results:
                raise ValueError(f"Missing dependency result for Task {dep_id}")

            dep_result = task_results[dep_id]

            context += (
                f"--- Task {dep_id} Result ---\n"
                f"{dep_result}\n\n"
            )

    # Add global memory (optional but powerful)
    context = global_context + context

    try:
        result = agent.execute(context, task.description)
    except Exception as e:
        result = f"[ERROR]: {str(e)}"

    task_results[task.id] = result
    task.updateTask(result)

    # Update global context
    global_context += f"\nTask {task.id} Output:\n{result}\n"

    print(f"[task {task.id}] result:\n{result}\n")