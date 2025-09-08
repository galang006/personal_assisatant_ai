# Personal AI Assistant Chatbot

This project implements a Python-based personal AI assistant chatbot that leverages LangChain and Ollama to provide a conversational experience with persistent memory capabilities. The assistant can save and retrieve user-specific facts and maintain chat history, making interactions more personalized and context-aware.

## Features
-   **Interactive Chat Interface**: A command-line interface for natural language interaction with the AI assistant.
-   **AI-Powered Conversational Agent**: Utilizes a LangChain ReAct agent for intelligent decision-making, tool usage, and response generation.
-   **Persistent Memory Management**: Capable of saving user-specific facts (e.g., hobbies, preferences, projects) into a vector database for later retrieval.
-   **Contextual Chat History**: Stores and manages conversation history using a vector database (Chroma DB) to provide the agent with relevant context for ongoing discussions.
-   **Local LLM Integration**: Designed to work with local Large Language Models (LLMs) via Ollama, supporting models like `llama3.1:8b` for generation and `nomic-embed-text:v1.5` for embeddings.
-   **Custom Tools**: Implements custom LangChain tools (`save_memory`, `search_memory`) that allow the agent to interact with its memory store.
-   **Configurable**: Easy to customize LLM models, database paths, and agent prompts through a dedicated configuration file.

## Installation

To set up and run the Personal AI Assistant Chatbot, follow these steps:

1.  **Clone the Repository (if applicable):**
    If you're starting from a GitHub repository, clone it first:
    ```bash
    git clone https://github.com/galang006/personal_assisatant_ai.git
    cd personal_assisatant_ai
    ```

2.  **Create a Virtual Environment:**
    It's recommended to use a virtual environment to manage dependencies.
    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install Python Dependencies:**
    Install the necessary Python libraries. Since no `requirements.txt` is provided, you'll need to install them manually:
    ```bash
    pip install langchain langchain-chroma langchain-ollama python-dotenv chromadb==0.4.24 # Specify chromadb version for compatibility
    ```

4.  **Install Ollama:**
    This project relies on Ollama for running local LLMs.
    -   Download and install Ollama from [ollama.com](https://ollama.com/download).

5.  **Pull Ollama Models:**
    Once Ollama is installed, pull the required models:
    ```bash
    ollama pull llama3.1:8b
    ollama pull nomic-embed-text:v1.5
    ```
    These models are specified in `config.py` for the LLM and embedding functions.

6.  **Create a `.env` file:**
    The project uses `python-dotenv` to load environment variables, though no specific variables are directly accessed from `.env` in the provided codebase except for `load_dotenv()` call. For future expansions or sensitive keys, you might add them here. For now, you can create an empty `.env` file in the root directory.
    ```bash
    touch .env
    ```

## Usage

To start a conversation with your personal AI assistant:

1.  Ensure all installation steps are completed and your virtual environment is active.
2.  Run the `main.py` script:
    ```bash
    python main.py
    ```

    You will see a greeting message:
    ```
    🤖Personal Assistant ChatBot🤖
    Type /quit to exit.
    ```

3.  **Interact with the Assistant:**
    Type your messages at the `🙂 User:` prompt. The assistant will respond, utilizing its memory and chat history.

    **Example Interaction:**

    ```
    🙂 User: Hi there, I like playing chess and reading fantasy books.
    🤖 Assistant: Saved to memory: "User likes playing chess and reading fantasy books." It's great to hear about your interests! Chess and fantasy books are both wonderful ways to engage your mind. What kind of fantasy books do you enjoy?
    🙂 User: I also work on a project about AI assistants.
    🤖 Assistant: Saved to memory: "User works on a project about AI assistants." That sounds fascinating! AI assistants are a rapidly evolving field. What specifically about your project are you working on?
    🙂 User: What are my hobbies?
    🤖 Assistant: You like playing chess and reading fantasy books.
    ```

4.  **Exit the Chat:**
    Type `/quit`, `/exit`, or `/bye` at any time to end the conversation.

### Testing Functionalities

The `test.py` file contains functions to directly test the memory agent and Chroma DB operations:

-   To test the memory agent's ability to save and retrieve information:
    ```python
    # Uncomment test_memory_agent() in main.py or run it directly
    # from test import test_memory_agent
    # test_memory_agent()
    ```
-   To directly search the Chroma DB for memories:
    ```python
    # Uncomment test_direct_chroma() in main.py or run it directly
    # from test import test_direct_chroma
    # test_direct_chroma("Large Language Model")
    ```
-   To view all saved memories:
    ```python
    # Uncomment get_all_memory() in main.py or run it directly
    # from test import get_all_memory
    # get_all_memory()
    ```

## Code Structure

The project is organized into several Python files, each responsible for a specific aspect of the AI assistant:

-   `.gitignore`: Specifies intentionally untracked files and directories that Git should ignore (e.g., `.env`, `database`, `__pycache__`).

-   `agent.py`:
    -   Defines the core LangChain ReAct agent.
    -   Integrates the `ChatOllama` LLM and custom tools (`save_memory`, `search_memory`).
    -   Configures the agent's prompt and execution settings.
    -   The `create_memory_agent()` function is responsible for initializing and returning the agent executor.

-   `chat.py`:
    -   Manages the main chat loop and user interaction.
    -   Handles retrieving recent chat history, invoking the AI agent with user input, and saving messages.
    -   The `invoke_agent()` function processes a single turn of conversation, and `chat_with_assistant()` runs the interactive chat session.

-   `config.py`:
    -   Centralized configuration file for the entire project.
    -   Defines constants such as `PERSIST_DIR` (for Chroma DB), `COLLECTION_NAME`, `DEFAULT_SESSION`, and `LLM_MODEL`.
    -   Contains the detailed `AGENT_PROMPT` that guides the AI assistant's behavior, rules, and tool usage.

-   `main.py`:
    -   The application's entry point.
    -   Loads environment variables using `dotenv`.
    -   Clears the console and initiates the `chat_with_assistant()` function to start the chatbot.
    -   Includes commented-out calls to testing functions from `test.py`.

-   `memory_manager.py`:
    -   Provides the `ChromaChatHistoryManager` class, which abstracts all interactions with the Chroma vector database.
    -   Handles saving new messages and memories (`save_message`).
    -   Searches for relevant memories based on a query (`search_memories`).
    -   Retrieves a session's complete chat history (`get_session_history`).
    -   Uses `OllamaEmbeddings` for converting text into vectors.

-   `test.py`:
    -   Contains utility functions for testing various components of the project.
    -   `test_memory_agent()`: Demonstrates how the agent uses `save_memory` and `search_memory`.
    -   `test_direct_chroma()`: Shows direct interaction with the `ChromaChatHistoryManager` for searching.
    -   `get_all_memory()`: Fetches and prints all documents and metadata stored in the Chroma DB.

-   `tools.py`:
    -   Defines custom LangChain tools used by the AI agent.
    -   `save_memory(memory_content: str)`: A tool for the agent to store significant user facts into the Chroma DB.
    -   `search_memory(query: str)`: A tool for the agent to retrieve relevant facts about the user from the Chroma DB based on a query.
    -   These tools wrap the functionalities provided by `memory_manager.py`.