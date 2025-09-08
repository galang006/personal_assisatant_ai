from datetime import datetime
from langchain.tools import tool
from memory_manager import ChromaChatHistoryManager
from config import DEFAULT_SESSION
import requests
from pydantic import BaseModel, Field
from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv

load_dotenv()

chat_manager = ChromaChatHistoryManager()

@tool("save_memory")
def save_memory(memory_content: str) -> str:
    """Store permanent facts about the user (projects, hobbies, likes, dislikes, preferences, etc.) in long-term memory. Use this when the user shares information worth remembering."""
    timestamp = datetime.now().isoformat()
    chat_manager.save_message(DEFAULT_SESSION, "memory", memory_content, timestamp)
    return f"Saved to memory: {memory_content}"

@tool("search_memory")
def search_memory(query: str) -> str:
    """Retrieve previously saved user memories. Use this when you need to recall details about the user’s preferences, past conversations, or stored facts."""
    memories = chat_manager.search_memories(query, DEFAULT_SESSION, k=3)
    if not memories:
        return f"No relevant memories for: {query}"
    return "\n".join(
        f"{i+1}. {m['content']} (from {m['metadata'].get('timestamp', 'Unknown')[:19]})"
        for i, m in enumerate(memories)
    )

class WikipediaArticleExporter(BaseModel):
    article: str = Field(description="The canonical name of the Wikipedia article")

@tool("wikipedia_text_exporter", args_schema=WikipediaArticleExporter, return_direct=False)
def wikipedia_text_exporter(article: str) -> str:
    """Fetch the introductory section of a Wikipedia article. Use this for general knowledge, background info, or explanations of well-known entities."""
    URL = "https://en.wikipedia.org/w/api.php"
    HEADERS = {"User-Agent": "MyBot/1.0"}
    
    params = {
        "action": "query",
        "list": "search",
        "srsearch": article,
        "format": "json"
    }
    
    try:
        response = requests.get(URL, params=params, headers=HEADERS, timeout=10).json()
        best_title = response["query"]["search"][0]["title"]
    except (KeyError, IndexError, requests.exceptions.RequestException):
        return f"No Wikipedia article found for '{article}'"
    
    extract_params = {
        "action": "query",
        "prop": "extracts",
        "exintro": True,
        "explaintext": True,
        "titles": best_title,
        "format": "json"
    }
    
    try:
        extract_response = requests.get(URL, params=extract_params, headers=HEADERS, timeout=10).json()
        pages = extract_response["query"]["pages"]
        page = next(iter(pages.values()))
        extract = page.get("extract", "No extract available")
        
        return f"Wikipedia article '{best_title}':\n{extract}"
        
    except (KeyError, requests.exceptions.RequestException):
        return f"Error retrieving content for '{best_title}'"
    
web_search_tool = TavilySearchResults(max_results=3)

@tool("search_web", return_direct=False)
def search_web(question: str):
    """Perform a live web search via Tavily for real-time or up-to-date information (e.g., current events, news, or facts not likely covered in Wikipedia)."""
    web_doct = web_search_tool.invoke({"query": question})
    web_result = "\n".join([doct["content"] for doct in web_doct])
    return web_result