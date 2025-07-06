import webbrowser
from duckduckgo_search import DDGS
from assistant.engine import LLMEngine

def search_web(query: str) -> str:
    results = DDGS().text(keywords=query, max_results=3)
    formatted_results = []
    for r in results:
        formatted_results.append(f"Title: {r["title"]}\nURL: {r["href"]}")
    return "\n\n".join(formatted_results)

def open_web(query: str):
    webbrowser.open(f"https://duckduckgo.com/?q={query}")
    return f"Opened web search for: {query}"

def summarize_text(text: str, llm_engine: LLMEngine) -> str:
    prompt = f"Summarize the following text concisely:\n\n{text}"
    summary = llm_engine.chat(prompt)
    return summary


