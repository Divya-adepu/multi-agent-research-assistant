# Multi-Agent Research Assistant

A multi-agent system that answers research questions by orchestrating three specialized agents using **LangGraph**: retrieval, summarization, and response generation.

## How it works

1. **Retrieval Agent** — searches the web (via DuckDuckGo) for information relevant to the user's query and returns raw results.
2. **Summarizer Agent** — condenses the raw search results into concise, structured key points using an LLM (Llama 3.1 via Groq).
3. **Response Generator Agent** — takes the summary and produces a clear, well-formatted final answer to the user's original question.

These agents are connected as nodes in a **LangGraph** state graph, with a shared state object passed between them at each step.
User Query
│
▼
[Retrieval Agent] → raw web search results
│
▼
[Summarizer Agent] → condensed key points
│
▼
[Response Generator Agent] → final formatted answer

## Why three separate agents?

Splitting the pipeline into distinct agents (rather than one large prompt) makes each step:
- **Easier to debug** — you can inspect the output of retrieval vs. summarization vs. generation independently
- **More modular** — any agent can be swapped out (e.g. a different search tool, or a different LLM) without touching the others
- **More reliable** — smaller, focused prompts tend to produce more consistent outputs than one large multi-task prompt

## Tech stack

- **LangGraph** — agent orchestration and state management
- **Groq API** (Llama 3.1 8B) — LLM inference
- **DuckDuckGo Search (`ddgs`)** — free web search, no API key required
- **Python-dotenv** — environment variable management

## Setup

1. Clone this repo
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux)
4. Install dependencies:
pip install langgraph langchain-groq ddgs python-dotenv groq
5. Create a `.env` file with your free Groq API key from console.groq.com:
GROQ_API_KEY=your_key_here
6. Run it:
python main.py

## Example
Enter your research question: what are the latest AI agent frameworks in 2026

The system retrieves current web results, summarizes them, and returns a clean, structured answer.

## Future improvements

- Streamlit web UI for a more interactive experience
- Error handling for failed searches or API calls
- Support for multi-turn conversations with memory