from datetime import datetime
from langchain.tools import tool
from memory_manager import ChromaChatHistoryManager
from config import DEFAULT_SESSION

chat_manager = ChromaChatHistoryManager()

@tool("save_memory")
def save_memory(memory_content: str) -> str:
    """Save facts about the user (projects, hobbies, likes, dislikes, etc.)."""
    timestamp = datetime.now().isoformat()
    chat_manager.save_message(DEFAULT_SESSION, "memory", memory_content, timestamp)
    return f"Saved to memory: {memory_content}"

@tool("search_memory")
def search_memory(query: str) -> str:
    """Retrieve facts about the user."""
    memories = chat_manager.search_memories(query, DEFAULT_SESSION, k=3)
    if not memories:
        return f"No relevant memories for: {query}"
    return "\n".join(
        f"{i+1}. {m['content']} (from {m['metadata'].get('timestamp', 'Unknown')[:19]})"
        for i, m in enumerate(memories)
    )