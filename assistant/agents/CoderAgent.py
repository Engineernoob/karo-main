
from assistant.agents.BaseAgent import BaseAgent
from assistant.engine import LLMEngine

class CoderAgent(BaseAgent):
    def __init__(self, llm_engine: LLMEngine):
        self.llm_engine = llm_engine

    def handle_task(self, task: str) -> str:
        prompt = f"""Generate code and provide an explanation for the following task. If it's a coding task, provide the code in a markdown code block. If it's a conceptual task, provide a clear explanation.

Task: {task}

Code/Explanation:"""
        response = self.llm_engine.chat(prompt)
        return response


