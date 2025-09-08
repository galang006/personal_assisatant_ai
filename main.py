import os
from chat import chat_with_assistant
from dotenv import load_dotenv
from test import test_direct_chroma, test_memory_agent, get_all_memory

load_dotenv()

if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    chat_with_assistant()
    #test_direct_chroma("Large Language Model")