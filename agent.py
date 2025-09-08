from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate
from langchain.agents import AgentExecutor, create_react_agent
from tools import save_memory, search_memory
from config import LLM_MODEL

def create_memory_agent():
    MEMORY_AGENT_PROMPT = """
    You are Megumi Kato my personal assistant.
    Stay in character: kind, soft-spoken, calm, supportive.
    Save important user facts using tools when needed.

    RULES:
    1. Always call save_memory when the user shares new personal info.
    2. Use search_memory to recall past facts.
    3. After using tools, respond naturally as Megumi.

    Tools:
    {tools}

    Previous conversation:
    {chat_history}

    New input: {input}
    {agent_scratchpad}
    """

    llm = ChatOllama(model=LLM_MODEL, temperature=0)
    tools = [save_memory, search_memory]

    promt = PromptTemplate(
        template=MEMORY_AGENT_PROMPT,
        input_types=["tools", "tool_names", "chat_history", "input", "agent_scratchpad"],
    )

    agent = create_react_agent(llm, tools, promt)

    return AgentExecutor(
        agent=agent, 
        tools=tools, 
        #verbose=True
        max_iterations=5,
        #max_execution_time=30,
        handle_parsing_errors=True
    )