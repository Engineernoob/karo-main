import os
import sys
from dotenv import load_dotenv
from assistant.agent import Agent
from assistant.duplex import start_duplex_conversation
from assistant.voice import listen_to_voice, speak

# Load environment variables from .env file
load_dotenv()

def main():
    print("🧠 Initializing Karo AI Assistant... Stand by.")
    print("🔹 Interface mode: Terminal")
    print("🔹 Type 'exit' to disengage.\n")

    use_voice = "--voice" in sys.argv

    agent = Agent(
        model=os.getenv("OLLAMA_MODEL", "dolphin-phi"),
        system_prompt_path="prompts/system.txt",
        memory_file="data/agent_memory.jsonl"
    )

    if use_voice:
        speak("Voice interface online. Say 'Hey Karo' to activate.")
        print("🎙️ Voice mode engaged. Awaiting wake word...")
        start_duplex_conversation(agent)
    else:
        while True:
            task = input("🪶 Awaiting your command: ")
            if task.lower() in ['exit', 'quit', 'shutdown']:
                print("🔻 Shutting down. Until next time.")
                break
            if task:
                print(f"📡 Routing task to Karo: '{task}'")
                agent.run(task)

if __name__ == "__main__":
    main()