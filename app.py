import os
from dotenv import load_dotenv
from assistant.agent import Agent
from assistant.voice import listen_to_voice
from assistant.background import BackgroundTaskManager
from assistant.duplex import start_duplex_conversation

# Load environment variables from .env file
load_dotenv()

def main():
    print("🧠 Karo.")
    print("• Speak your command, or type it below.")
    print("• Say or type 'exit' to quit.\n")

    # 1) Setup background task manager
    bg_manager = BackgroundTaskManager()

    # 2) Instantiate Agent with background manager
    agent = Agent(
        model=os.getenv("OLLAMA_MODEL", "dolphin-phi"),
        system_prompt_path="prompts/system.txt",
        memory_file="data/agent_memory.jsonl"
    )

    # 3) Main loop: auto-detect voice or text
    while True:
        task = listen_to_voice().strip()
        if not task:
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