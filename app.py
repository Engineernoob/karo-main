import os
import sys
from dotenv import load_dotenv
from assistant.agent import Agent
from assistant.voice import listen_to_voice, speak

# Load environment variables from .env file
load_dotenv()

def karo_voice_loop(agent: Agent):
    """Full voice-driven interaction loop."""
    speak("Voice mode activated. I'm listening.")
    while True:
        query = listen_to_voice()
        if not query:
            continue
        if query.lower() in ["exit", "quit", "stop karo"]:
            speak("Goodbye.")
            break

        print(f"\n🎯 High-level voice task: {query}")
        agent.run(query)  # optionally capture response if you want to speak it

def main():
    print("Welcome to Karo AI Assistant!")
    print("Type 'exit' to quit.")

    use_voice = "--voice" in sys.argv

    agent = Agent(
        model=os.getenv("OLLAMA_MODEL", "dolphin-phi"),
        system_prompt_path="prompts/system.txt",
        memory_file="data/agent_memory.jsonl"
    )

    if use_voice:
        karo_voice_loop(agent)
    else:
        while True:
            task = input("\nEnter a high-level task for Karo: ")
            if task.lower() == 'exit':
                break
            if task:
                agent.run(task)

if __name__ == "__main__":
    main()