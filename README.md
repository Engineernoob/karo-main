
# Karo AI Assistant

Karo is a local, voice-capable, uncensored AI agent designed to serve as an extension of the user's mind. It combines the calm intelligence of Jarvis, the execution focus of Manus, and the linguistic fluidity of GPT.

## Features

- **Agent Mode**: Decomposes high-level tasks into subtasks, reasons through them, and executes solutions step-by-step.
- **Modular Structure**: Organized into `app.py`, `prompts/`, `assistant/`, and `data/` for clear separation of concerns.
- **Local LLM Integration**: Utilizes the `dolphin-phi` model via Ollama for uncensored, local AI processing.
- **Memory**: Logs and recalls past tasks and their results.
- **Future-Ready**: Designed for easy integration with GUI, TTS, and advanced tool execution.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd karo
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure Ollama is running and the `dolphin-phi` model is available. If not, download it:
   ```bash
   ollama pull dolphin-phi
   ```

## Usage

To start Karo, run:

```bash
python app.py
```

Then, enter your high-level tasks at the prompt.

## Project Structure

```
karo/
├── app.py                      # CLI entry point
├── prompts/system.txt          # Persona: Karo = Jarvis × Manus × GPT hybrid
├── assistant/
│   ├── agent.py                # Main agent loop: runs planner + executor
│   ├── planner.py              # Uses LLM to break high-level task into subtasks
│   ├── executor.py             # Handles codegen, reasoning, file outputs
│   ├── memory.py               # Logs and recalls past tasks
│   ├── engine.py               # Wrapper for ollama.chat() with history + system prompt
│   └── tools.py                # Future plugin system: @code, @summarize, etc.
├── data/agent_memory.jsonl     # Persistent log of subtasks + results
├── requirements.txt
└── README.md
```


