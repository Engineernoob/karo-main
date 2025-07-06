from assistant.agents.BaseAgent import BaseAgent
from assistant.engine import LLMEngine

class PlannerAgent(BaseAgent):
    def __init__(self, llm_engine: LLMEngine):
        self.llm_engine = llm_engine

    def handle_task(self, high_level_task: str) -> str:
        prompt = f"""Given the high-level task: "{high_level_task}", break it down into a list of smaller, actionable subtasks. Each subtask should be a concise, single sentence. Return only the list of subtasks, one per line, without any additional text or numbering.

Example:
High-level task: "Create a CLI todo app"
Subtasks:
Define the data structure for a todo item.
Implement functions to add, list, and mark todo items as complete.
Create a command-line interface for user interaction.
Add persistence to save and load todo items.

High-level task: "{high_level_task}"
Subtasks:"""
        response = self.llm_engine.chat(prompt)
        return "\n".join([subtask.strip() for subtask in response.split("\n") if subtask.strip()])


