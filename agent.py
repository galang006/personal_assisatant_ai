from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate
from langchain.agents import AgentExecutor, create_react_agent
from tools import save_memory, search_memory
from config import LLM_MODEL, AGENT_PROMPT

def create_memory_agent():
    llm = ChatOllama(model=LLM_MODEL, temperature=0)
    tools = [save_memory, search_memory]

    promt = PromptTemplate(
        template=AGENT_PROMPT,
        input_variables=["tools", "tool_names", "chat_history", "input", "agent_scratchpad"],
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