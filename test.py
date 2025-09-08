from agent import create_memory_agent
from memory_manager import ChromaChatHistoryManager
from agent import create_memory_agent

chat_manager = ChromaChatHistoryManager()

def test_memory_agent():
    """Test agent-based approach"""
    print("=== Testing Memory Agent ===")
    
    agent_executor = create_memory_agent()
    
    try:
        # Save some memories
        result1 = agent_executor.invoke({
            "input": "The game I like is Football Manager 2024.",
            "chat_history": ""
        })
        print(f"Save result: {result1['output']}")
        
        # Search memories
        result2 = agent_executor.invoke({
            "input": "Can you tell me what games I like?",
            "chat_history": ""
        })
        print(f"Search result: {result2['output']}")
        
    except Exception as e:
        print(f"Agent failed: {e}")

def test_direct_chroma(input: str, session_id: str = None):
    """Test Chroma DB directly"""
    print("=== Testing Direct Chroma Operations ===")
    
    memories = chat_manager.search_memories(input, session_id)
    print(f"Found {len(memories)} memories:")
    for memory in memories:
        print(f"  - {memory['content']}")

def get_all_memory():
    """
        Get all memory from Chroma DB
    """
    all_data = chat_manager.store.get(include=["documents", "metadatas"])
    for i, doc in enumerate(all_data["documents"]):
        print(f"[{i}] {doc} -> {all_data['metadatas'][i]}")