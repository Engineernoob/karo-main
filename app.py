import os
import sys
from dotenv import load_dotenv
from assistant.agent import Agent
from assistant.voice import listen_to_voice, speak

# Load environment variables from .env file
load_dotenv()

def main():
    print("Welcome to Karo AI Assistant!")
    print("Type 'exit' to quit.")

    use_voice = "--voice" in sys.argv

    agent = Agent(
        model=os.getenv("OLLAMA_MODEL", "dolphin-phi"),
        system_prompt_path = "prompts/system.txt",
        memory_file="karo-main/data/agent_memory.jsonl"
    )

    while True:
        if use_voice:
            task = listen_to_voice()
        else:
            task = input("\nEnter a high-level task for Karo: ")

        if task.lower() == 'exit':
            if use_voice:
                speak("Goodbye!")
            break
        
        if task:
            agent.run(task)
            # In a real voice application, you might want to capture Karo's final response
            # and speak it aloud. For now, the agent's print statements will suffice.
            # If you want to speak the final summary of the task, you'd need to modify
            # agent.py to return a summary or have a dedicated speaking function.

if __name__ == "__main__":
    main()


