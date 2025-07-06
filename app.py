import os
from dotenv import load_dotenv
from assistant.agent import Agent
from assistant.voice import listen_to_voice
from assistant.background import BackgroundTaskManager

# Load environment variables from .env file
load_dotenv()

def main():
    print("🧠 Karo.")
    print("• Speak your command, or type it below.")
    print("• Say or type 'exit' to quit.\n")

    bg_manager = BackgroundTaskManager()

    agent = Agent(
        model=os.getenv("OLLAMA_MODEL", "dolphin-phi"),
        system_prompt_path="prompts/system.txt",
        memory_file="data/agent_memory.jsonl",
        bg=bg_manager
    )

    while True:
        task = listen_to_voice().strip()
        if not task:
            task = input("🪶 Enter command: ").strip()

        if not task:
            continue
        if task.lower() in ("exit", "quit", "shutdown"):
            print("🔻 Shutting down. Goodbye.")
            break

        print("\n🤔 Karo is thinking...")
        response = agent.run(task)  # run() should return Karo's final response string

        if response:
            print(f"\nKaro: {response}\n")

if __name__ == "__main__":
    main()