import webbrowser
import subprocess
import psutil
from duckduckgo_search import DDGS
from assistant.engine import LLMEngine

def search_web(query: str) -> str:
    results = DDGS().text(keywords=query, max_results=3)
    formatted_results = []
    for r in results:
        formatted_results.append(f"Title: {r['title']}\nURL: {r['href']}")
    return "\n\n".join(formatted_results)

def open_web(query: str):
    webbrowser.open(f"https://duckduckgo.com/?q={query}")
    return f"Opened web search for: {query}"

def summarize_text(text: str, llm_engine: LLMEngine) -> str:
    prompt = f"Summarize the following text concisely:\n\n{text}"
    summary = llm_engine.chat(prompt)
    return summary

def open_app(app_name: str) -> str:
    """Opens a specified application. Note: This is OS-dependent and might require specific commands."""
    try:
        if os.name == 'posix': # macOS, Linux, Unix
            subprocess.Popen([app_name])
        elif os.name == 'nt': # Windows
            os.startfile(app_name)
        else:
            return f"Unsupported operating system for opening applications: {os.name}"
        return f"Attempted to open {app_name}."
    except FileNotFoundError:
        return f"Application \'{app_name}\' not found. Please ensure it is in your system\'s PATH."
    except Exception as e:
        return f"Error opening {app_name}: {e}"

def read_email() -> str:
    """Placeholder for reading emails. Requires integration with an email API (e.g., Gmail API, Outlook API)."""
    return "Reading emails is a complex task that requires integration with a specific email service API (e.g., Gmail, Outlook). This functionality is not yet implemented. Please read your emails manually."

def system_stats() -> str:
    """Retrieves current system statistics (CPU, Memory, Disk)."""
    cpu_percent = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    disk_usage = psutil.disk_usage("/")

    stats = (
        f"CPU Usage: {cpu_percent:.1f}%\n"
        f"Memory Usage: {memory_info.percent:.1f}% ({memory_info.used / (1024**3):.2f} GB used / {memory_info.total / (1024**3):.2f} GB total)\n"
        f"Disk Usage: {disk_usage.percent:.1f}% ({disk_usage.used / (1024**3):.2f} GB used / {disk_usage.total / (1024**3):.2f} GB total)"
    )
    return stats