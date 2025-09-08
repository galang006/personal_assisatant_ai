from memory_manager import ChromaChatHistoryManager
from agent import create_memory_agent
from config import DEFAULT_SESSION

chat_manager = ChromaChatHistoryManager()

def invoke_agent(agent, session_id, user_input):
    recent_history = chat_manager.get_session_history(session_id, limit = 10)
    history_text = "\n".join(f"{m['role']}: {m['content']}" for m in recent_history)

    chat_manager.save_message(session_id, "user", user_input)
    response = agent.invoke(
        {
            "input": user_input,
            "chat_history": history_text
        }
    )["output"]
    chat_manager.save_message(session_id, "assistant", response)
    return response

def chat_with_assistant():
    recent_history = chat_manager.get_session_history(DEFAULT_SESSION, limit = 10)

    agent = create_memory_agent()

    print("🤖Personal Assistant ChatBot🤖 \nType /quit to exit.\n")

    for m in recent_history:
        if m['role'] == "user":
            print(f"🙂 User: {m['content']}")
        elif m['role'] == "assistant":
            print(f"🤖 Assistant: {m['content']}")

    while True:
        msg = input("🙂 User: ")
        if msg.lower() in ["/quit", "/exit", "/bye"]:
            print("Exiting chat. Goodbye!")
            break
        
        reply = invoke_agent(agent, DEFAULT_SESSION, msg)
        print(f"🤖 Assistant: {reply}")