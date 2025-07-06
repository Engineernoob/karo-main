import ollama

class LLMEngine:
    def __init__(self, model="dolphin-phi", system_prompt_path="prompts/system.txt"):
        self.model = model
        self.history = []
        self.system_prompt = self._load_system_prompt(system_prompt_path)
        self.context = ""

    def _load_system_prompt(self, path):
        with open(path, "r") as f:
            return f.read()

    def add_context(self, context: str):
        self.context = context

    def chat(self, prompt):
        messages = [
            {"role": "system", "content": self.system_prompt},
        ]
        if self.context:
            messages.append({"role": "system", "content": self.context})
        messages.extend(self.history)
        messages.append({"role": "user", "content": prompt})

        response = ollama.chat(model=self.model, messages=messages)
        self.history.append({"role": "user", "content": prompt})
        self.history.append({"role": "assistant", "content": response["message"]["content"]})
        return response["message"]["content"]


