import os
import sys
from dotenv import load_dotenv
from assistant.agent import Agent
from assistant.voice import listen_to_voice

# Load environment variables from .env file
load_dotenv()

def main():
    print("🧠 Karo.")
    print("• Speak your command, or type it below.")
    print("• Say or type 'exit' to quit.\n")

    agent = Agent(
        model=os.getenv("OLLAMA_MODEL", "dolphin-phi"),
        system_prompt_path="prompts/system.txt",
        memory_file="data/agent_memory.jsonl"
    )

    while True:
        # Try to capture a voice command first
        task = listen_to_voice().strip()
        if not task:
            # No speech detected—fall back to text input
            task = input("🪶 Enter command: ").strip()

        if not task:
            continue
        if task.lower() in ("exit", "quit", "shutdown"):
            print("🔻 Shutting down. Goodbye.")
            break

        print(f"📡 Processing: {task}")
        agent.run(task)

if __name__ == "__main__":
    main()