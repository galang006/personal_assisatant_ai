import os
from chat import chat_with_assistant
from dotenv import load_dotenv
load_dotenv()

if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    chat_with_assistant()
