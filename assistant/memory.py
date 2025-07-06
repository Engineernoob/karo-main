import json

class AgentMemory:
    def __init__(self, memory_file="karo-main/data/agent_memory.jsonl"):
        self.memory_file = memory_file

    def add_task_result(self, task: str, result: str):
        with open(self.memory_file, "a") as f:
            json.dump({"task": task, "result": result}, f)
            f.write("\n")

    def recall(self) -> list[dict]:
        memories = []
        try:
            with open(self.memory_file, "r") as f:
                for line in f:
                    memories.append(json.loads(line))
        except FileNotFoundError:
            pass
        return memories


