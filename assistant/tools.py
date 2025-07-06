import os
import webbrowser
import subprocess
import psutil
from duckduckgo_search import DDGS
from assistant.engine import LLMEngine

def search_web(query: str) -> str:
    """
    Perform a DuckDuckGo search and return the top 3 result titles and URLs.
    """
    results = DDGS().text(keywords=query, max_results=3)
    formatted = []
    for r in results:
        formatted.append(f"Title: {r['title']}\nURL: {r['href']}")
    return "\n\n".join(formatted)

def open_web(query: str) -> str:
    """
    Launches a browser search for the given query.
    """
    url = f"https://duckduckgo.com/?q={query}"
    webbrowser.open(url)
    return f"Opened web search for: {query}"

def summarize_text(text: str, llm_engine: LLMEngine) -> str:
    """
    Summarize the given text using the provided LLM engine.
    """
    prompt = f"Summarize the following text concisely:\n\n{text}"
    return llm_engine.chat(prompt)

def open_app(app_name: str) -> str:
    """
    Opens a specified application (OS-dependent). Returns status message.
    """
    try:
        if os.name == 'posix':  # macOS, Linux, Unix
            subprocess.Popen([app_name])
        elif os.name == 'nt':   # Windows
            os.startfile(app_name)
        else:
            return f"Unsupported OS: {os.name}"
        return f"Attempted to open application: {app_name}"
    except FileNotFoundError:
        return f"Application '{app_name}' not found. Ensure it's in your PATH."
    except Exception as e:
        return f"Error opening '{app_name}': {e}"

def read_email() -> str:
    """
    Placeholder: Returns a stub message about email integration status.
    """
    return (
        "Reading emails requires an email API (e.g., Gmail API). "
        "This function is not yet implemented."
    )

def system_stats() -> str:
    """
    Retrieves and returns current CPU, memory, and disk usage stats.
    """
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    return (
        f"CPU Usage: {cpu:.1f}%\n"
        f"Memory Usage: {mem.percent:.1f}% "
        f"({mem.used / 2**30:.2f}GB / {mem.total / 2**30:.2f}GB)\n"
        f"Disk Usage: {disk.percent:.1f}% "
        f"({disk.used / 2**30:.2f}GB / {disk.total / 2**30:.2f}GB)"
    )