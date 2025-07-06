
from assistant.agents.BaseAgent import BaseAgent
from assistant.engine import LLMEngine
from assistant import tools

class ResearchAgent(BaseAgent):
    def __init__(self, llm_engine: LLMEngine):
        self.llm_engine = llm_engine

    def handle_task(self, task: str) -> str:
        if task.startswith("@search "):
            query = task.replace("@search ", "").strip()
            print(f"ResearchAgent: Executing web search for: {query}")
            return tools.search_web(query)
        elif task.startswith("@summarize "):
            text_to_summarize = task.replace("@summarize ", "").strip()
            print(f"ResearchAgent: Summarizing text...")
            return tools.summarize_text(text_to_summarize, self.llm_engine)
        else:
            # Default research behavior if no specific tool command is given
            prompt = f"""Perform research on the following topic. Provide a concise summary of your findings.

Topic: {task}

Research Summary:"""
            response = self.llm_engine.chat(prompt)
            return response


