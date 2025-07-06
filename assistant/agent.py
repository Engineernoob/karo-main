from assistant.memory import AgentMemory
from assistant.engine import LLMEngine
from assistant.agent_router import route_task
from assistant.semantic_memory import SemanticMemory
from assistant.background import BackgroundTaskManager
from assistant.tools import search_web, open_web, open_app

class Agent:
    def __init__(
        self,
        model="dolphin-phi",
        system_prompt_path="prompts/system.txt",
        memory_file="data/agent_memory.jsonl",
        bg: BackgroundTaskManager = None,
        listener=None
    ):
        self.llm_engine = LLMEngine(model=model, system_prompt_path=system_prompt_path)
        self.memory = AgentMemory(memory_file=memory_file)
        self.semantic_memory = SemanticMemory()
        # Use provided or create a background manager
        self.bg = bg or BackgroundTaskManager()
        self.listener = listener

    def classify_intent(self, text: str) -> str:
        prompt = (
            "Classify the following user input into one of two categories: "
            "\"conversational\" or \"task\".\n\n"
            f"Input: \"{text}\"\n"
            "Output:"
        )
        response = self.llm_engine.chat(prompt)
        cls = response.strip().lower()
        if "conversational" in cls:
            return "conversational"
        return "task"

    def run(self, high_level_task: str) -> str:
        task = high_level_task.strip()
        lower = task.lower()

        # ----- Background task controls -----
        if lower == "list tasks":
            tasks = self.bg.list_tasks()
            if not tasks:
                resp = "No background tasks."
            else:
                resp = "Background tasks:\n" + "\n".join(
                    f"{t['name']} (#{tid}): {t['status']}"
                    for tid, t in self.bg.metadata.items()
                )
            print(f"Karo: {resp}")
            return resp

        if lower.startswith("status of task "):
            tid = lower.split("status of task ", 1)[1]
            info = self.bg.get_status(tid)
            resp = f"Task #{tid}: {info}" if info else f"No such task #{tid}."
            print(f"Karo: {resp}")
            return resp

        if lower.startswith("cancel task "):
            tid = lower.split("cancel task ", 1)[1]
            ok = self.bg.cancel_task(tid)
            resp = f"Cancelled task #{tid}." if ok else f"Unable to cancel task #{tid}."
            print(f"Karo: {resp}")
            return resp

        # ----- Offload specific long-running tools -----
        if lower.startswith("search for "):
            query = task[len("search for "):].strip()
            tid = self.bg.add_task(f"Search: {query}", search_web, query)
            resp = f"I've started background search task #{tid} for '{query}'."
            print(f"Karo: {resp}")
            return resp

        # ----- Intent classification -----
        intent = self.classify_intent(task)
        if intent == "conversational":
            print(f"\nKaro: Detected conversational input.")
            response = self.llm_engine.chat(task)
            print(f"Karo: {response}")
            return response

        # ----- Task planning flow -----
        print(f"\nKaro: Received high-level task: '{task}'")

        # Episodic memory context
        past = self.memory.recall()
        if past:
            print("Karo: Recalling past tasks for context...")
            ctx = "Past tasks and results:\n" + "\n".join(f"- {m['task']}: {m['result']}" for m in past)
            self.llm_engine.add_context(ctx)

        # Semantic memory context
        sem = self.semantic_memory.search_memory(task)
        if sem:
            print("Karo: Found relevant semantic memories...")
            sem_ctx = "Relevant past knowledge:\n" + "\n".join(sem)
            self.llm_engine.add_context(sem_ctx)

        # Delegate to appropriate agent
        initial = route_task(task, self.llm_engine)
        print(f"Karo: Routing to {type(initial).__name__}.")
        result = initial.handle_task(task)

        # Planner handling
        planner_example = route_task("plan a task", self.llm_engine)
        if isinstance(initial, type(planner_example)):
            lines = [l.strip() for l in result.split("\n") if l.strip()]
            if not lines:
                msg = "Could not break down the task. Try rephrasing."
                print(f"Karo: {msg}")
                return msg

            print("Karo: Subtasks:")
            for i, sub in enumerate(lines, 1):
                print(f"  {i}. {sub}")

            for i, sub in enumerate(lines, 1):
                print(f"\nKaro: Executing subtask {i}/{len(lines)}: '{sub}'")
                agent = route_task(sub, self.llm_engine)
                print(f"Karo: → {type(agent).__name__}")
                sub_res = agent.handle_task(sub)
                print(f"Karo: Result:\n{sub_res}")
                self.memory.add_task_result(sub, sub_res)
                self.semantic_memory.add_to_memory(f"Task: {sub}\nResult: {sub_res}")

            print("\nKaro: All subtasks completed.")
            return "All subtasks completed."

        # Non-planner final
        print(f"Karo: Final result:\n{result}")
        self.memory.add_task_result(task, result)
        self.semantic_memory.add_to_memory(f"Task: {task}\nResult: {result}")
        return result