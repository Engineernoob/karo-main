from assistant.agents.PlannerAgent import PlannerAgent
from assistant.agents.CoderAgent import CoderAgent
from assistant.agents.ResearchAgent import ResearchAgent
from assistant.agents.ReviewAgent import ReviewAgent
from assistant.engine import LLMEngine

def route_task(task: str, llm_engine: LLMEngine):
    # If the task looks like a search
    if "@search" in task or "find" in task.lower() or "research" in task.lower():
        return ResearchAgent(llm_engine)
    elif "@code" in task or "code" in task.lower() or "implement" in task.lower() or "generate" in task.lower():
        return CoderAgent(llm_engine)
    elif "review" in task.lower() or "critique" in task.lower() or "improve" in task.lower():
        return ReviewAgent(llm_engine)
    else:
        return PlannerAgent(llm_engine)


