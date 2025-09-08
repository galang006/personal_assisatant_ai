import uuid
from datetime import datetime
from typing import List, Dict
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from config import PERSIST_DIR, COLLECTION_NAME

class ChromaChatHistoryManager:
    def __init__(self, persist_directory = PERSIST_DIR, collection_name = COLLECTION_NAME):
        self.embed_model = OllamaEmbeddings(model="nomic-embed-text:v1.5")
        self.store = Chroma(
            persist_directory= persist_directory,
            embedding_function= self.embed_model,
            collection_name= collection_name
        )

    def save_message(self, session_id: str, role: str, content: str, timestamp: str = None):
        if timestamp is None:
            timestamp = datetime.now().isoformat()
        message_id = str(uuid.uuid4())

        metadata = {
            "session_id": session_id,
            "role": role,
            "timestamp": timestamp,
            "message_id": message_id,
        }
        searchable_text = f"{role}: {content}"

        self.store.add_texts([searchable_text], [metadata], [message_id])
        return True
    
    def search_memory(self, query: str,session_id: str = None, k: int = 5) -> List[Dict]:
        filter_dict = {"session_id":session_id} if session_id else {}
        results =  self.store.similarity_search(query=query, k=k, filter=filter_dict)
        return [
            {"content": r.page_content, "metadata": r.metadata, "relevance_score": "high"}
            for r in results
        ]
    
    def get_session_history(self, session_id: str, limit: int = 50) -> List[Dict]:
        results = self.store.get(
            where= {"session_id": session_id},
            limit= limit,
            include=["metadata", "documents"]
        )

        messages = [
            {
                "role": m["role"],
                "content": d[len(m["role"]) + 2:] if d.startswith(m["role"] + ": ") else d,
                "timestamp": m["timestamp"],
                "message_id": m["message_id"]
            }
            for d,m in zip(results["documents"], results["metadata"])
        ]

        messages.sort(key=lambda x: x["timestamp"])

        return messages