from assistant.memory import AgentMemory
from assistant.engine import LLMEngine
from assistant.agent_router import route_task
from assistant.semantic_memory import SemanticMemory

class Agent:
    def __init__(self, model="dolphin-phi", system_prompt_path="prompts/system.txt", memory_file="data/agent_memory.jsonl", bg=None, listener=None):
        self.llm_engine = LLMEngine(model=model, system_prompt_path=system_prompt_path)
        self.memory = AgentMemory(memory_file=memory_file)
        self.semantic_memory = SemanticMemory() # Initialize semantic memory
        self.bg = bg  # Background task for the agent (e.g., monitoring sensors)
       self.listener = listener  # Listener for tasks or events

    def run(self, high_level_task: str):
        print(f"\nKaro: Received high-level task: \'{high_level_task}\'")
        
        # Recall past memories (JSONL) and provide them to the LLM engine for context
        past_memories = self.memory.recall()
        if past_memories:
            print("Karo: Recalling past tasks and results for context...")
            memory_context = "\nPast tasks and their results:\n"
            for mem in past_memories:
                memory_context += f"- Task: {mem['task']}\n  Result: {mem['result']}\n"
            self.llm_engine.add_context(memory_context) # Add context to LLM engine

        # Search semantic memory for relevant context based on the high-level task
        semantic_results = self.semantic_memory.search_memory(high_level_task)
        if semantic_results:
            print("Karo: Found relevant semantic memories...")
            semantic_context = "\nRelevant past knowledge:\n" + "\n".join(semantic_results)
            self.llm_engine.add_context(semantic_context) # Add semantic context to LLM engine

        # Route the initial high-level task to the appropriate agent
        initial_agent = route_task(high_level_task, self.llm_engine)
        print(f"Karo: Routing initial task to {type(initial_agent).__name__}.")
        
        initial_response = initial_agent.handle_task(high_level_task)
        
        # If the initial agent is a PlannerAgent, its response will be subtasks
        if isinstance(initial_agent, type(route_task("plan a task", self.llm_engine))): # Check if it's a PlannerAgent
            subtasks = [s.strip() for s in initial_response.split('\n') if s.strip()]
            if not subtasks:
                print("Karo: Could not break down the task into subtasks. Please try a different task.")
                return

            print("Karo: Subtasks identified:")
            for i, subtask in enumerate(subtasks):
                print(f"  {i+1}. {subtask}")

            for i, subtask in enumerate(subtasks):
                print(f"\nKaro: Executing subtask {i+1}/{len(subtasks)}: \'{subtask}\'")
                # Route each subtask to the appropriate agent for execution
                current_agent = route_task(subtask, self.llm_engine)
                print(f"Karo: Routing subtask to {type(current_agent).__name__}.")
                result = current_agent.handle_task(subtask)
                print(f"Karo: Subtask result:\n{result}")
                self.memory.add_task_result(subtask, result)
                self.semantic_memory.add_to_memory(f"Task: {subtask}\nResult: {result}") # Add to semantic memory
            
            print("\nKaro: Task completed. All subtasks executed and logged.")
        else:
            # If the initial agent was not a PlannerAgent (e.g., ResearchAgent for a direct search query)
            # then its response is the final result for the high-level task.
            print(f"Karo: Task completed by {type(initial_agent).__name__}. Result:\n{initial_response}")
            self.memory.add_task_result(high_level_task, initial_response)
            self.semantic_memory.add_to_memory(f"Task: {high_level_task}\nResult: {initial_response}") # Add to semantic memory


