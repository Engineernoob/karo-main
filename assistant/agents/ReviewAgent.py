
from assistant.agents.BaseAgent import BaseAgent
from assistant.engine import LLMEngine

class ReviewAgent(BaseAgent):
    def __init__(self, llm_engine: LLMEngine):
        self.llm_engine = llm_engine

    def handle_task(self, task: str) -> str:
        prompt = f"""Review and critique the following input. Provide constructive feedback and suggestions for improvement.

Input to review: {task}

Review and Improvement:"""
        response = self.llm_engine.chat(prompt)
        return response


