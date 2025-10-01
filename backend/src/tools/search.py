"""Web search tool using Tavily."""
from langchain_core.tools import tool
from langchain_tavily import TavilySearch
from ..config import settings


@tool
def web_search(user_input: str) -> str:
    """
    Search the web using Tavily and return stitched text results.

    Args:
        user_input: The search query string

    Returns:
        Combined text content from search results, or "No results found."
    """
    ts = TavilySearch(max_results=settings.TAVILY_MAX_RESULTS)
    resp = ts.invoke({"query": user_input})
    chunks = [r.get("content") for r in resp.get("results", []) if r.get("content")]
    return "\n\n".join(chunks) or "No results found."
