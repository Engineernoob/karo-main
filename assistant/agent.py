from assistant.memory import AgentMemory
from assistant.engine import LLMEngine
from assistant.agent_router import route_task
from assistant.semantic_memory import SemanticMemory

class Agent:
    def __init__(
        self,
        model="dolphin-phi",
        system_prompt_path="prompts/system.txt",
        memory_file="data/agent_memory.jsonl",
        bg=None,
        listener=None
    ):
        self.llm_engine = LLMEngine(model=model, system_prompt_path=system_prompt_path)
        self.memory = AgentMemory(memory_file=memory_file)
        self.semantic_memory = SemanticMemory()
        self.bg = bg
        self.listener = listener

    def classify_intent(self, text: str) -> str:
        prompt = (
            "Classify the following user input into one of two categories: "
            "\"conversational\" or \"task\".\n\n"
            f"Input: \"{text}\"\n"
            "Output:"
        )
        response = self.llm_engine.chat(prompt)
        classification = response.strip().lower()
        if "conversational" in classification:
            return "conversational"
        elif "task" in classification:
            return "task"
        return "task"

    def run(self, high_level_task: str) -> str:
        intent = self.classify_intent(high_level_task)

        # Conversational shortcut
        if intent == "conversational":
            print(f"\nKaro: Detected conversational input.")
            response = self.llm_engine.chat(high_level_task)
            print(f"Karo: {response}")
            return response

        # Otherwise, actionable task flow
        print(f"\nKaro: Received high-level task: '{high_level_task}'")

        # Add episodic memory context
        past = self.memory.recall()
        if past:
            print("Karo: Recalling past tasks for context...")
            ctx = "\nPast tasks and results:\n"
            for m in past:
                ctx += f"- {m['task']}: {m['result']}\n"
            self.llm_engine.add_context(ctx)

        # Add semantic memory context
        sem = self.semantic_memory.search_memory(high_level_task)
        if sem:
            print("Karo: Found relevant semantic memories...")
            sem_ctx = "\nRelevant past knowledge:\n" + "\n".join(sem)
            self.llm_engine.add_context(sem_ctx)

        # Delegate to appropriate agent
        initial = route_task(high_level_task, self.llm_engine)
        print(f"Karo: Routing to {type(initial).__name__}.")
        result = initial.handle_task(high_level_task)

        # If it's a planner, break into subtasks
        planner_example = route_task("plan a task", self.llm_engine)
        if isinstance(initial, type(planner_example)):
            lines = [l.strip() for l in result.split("\n") if l.strip()]
            if not lines:
                print("Karo: Couldn't decompose the task. Try rephrasing.")
                return ""

            print("Karo: Subtasks:")
            for idx, sub in enumerate(lines, 1):
                print(f"  {idx}. {sub}")

            for idx, sub in enumerate(lines, 1):
                print(f"\nKaro: Executing subtask {idx}/{len(lines)}: '{sub}'")
                agent = route_task(sub, self.llm_engine)
                print(f"Karo: → {type(agent).__name__}")
                sub_res = agent.handle_task(sub)
                print(f"Karo: Result:\n{sub_res}")
                self.memory.add_task_result(sub, sub_res)
                self.semantic_memory.add_to_memory(f"Task: {sub}\nResult: {sub_res}")

            print("\nKaro: All subtasks completed.")
            return "All subtasks completed."

        # Non-planner final result
        print(f"Karo: Final result:\n{result}")
        self.memory.add_task_result(high_level_task, result)
        self.semantic_memory.add_to_memory(f"Task: {high_level_task}\nResult: {result}")
        return result