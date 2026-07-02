# Multi-Agent Research Assistant

A multi-agent system that answers research questions by orchestrating three specialized agents using **LangGraph**: retrieval, summarization, and response generation. Includes a custom Streamlit web interface.

## How it works

1. **Retrieval Agent** — searches the web (via DuckDuckGo) for information relevant to the user's query and returns raw results.
2. **Summarizer Agent** — condenses the raw search results into concise, structured key points using an LLM (Llama 3.1 via Groq).
3. **Response Generator Agent** — takes the summary and produces a clear, well-formatted final answer to the user's original question.

These agents are connected as nodes in a **LangGraph** state graph, with a shared state object passed between them at each step.

    User Query
        |
        v
    [Retrieval Agent] --> raw web search results
        |
        v
    [Summarizer Agent] --> condensed key points
        |
        v
    [Response Generator Agent] --> final formatted answer

## Why three separate agents?

Splitting the pipeline into distinct agents (rather than one large prompt) makes each step:
- **Easier to debug** — you can inspect the output of retrieval vs. summarization vs. generation independently
- **More modular** — any agent can be swapped out (e.g. a different search tool, or a different LLM) without touching the others
- **More reliable** — smaller, focused prompts tend to produce more consistent outputs than one large multi-task prompt

## Web interface

The app includes a Streamlit UI with a clean, custom-designed dashboard: input a question, watch the agents run, and get a formatted answer with an expandable section showing each agent's intermediate output (the raw search results and the summary).

## Tech stack

- **LangGraph** — agent orchestration and state management
- **Groq API** (Llama 3.1 8B) — LLM inference
- **DuckDuckGo Search (`ddgs`)** — free web search, no API key required
- **Streamlit** — web interface
- **Python-dotenv** — environment variable management

## Setup

1. Clone this repo
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux)
4. Install dependencies:
pip install -r requirements.txt
5. Create a `.env` file with your free Groq API key from console.groq.com:
GROQ_API_KEY=your_key_here
6. Run the terminal version:
python main.py
   Or run the web interface:
streamlit run app.py

## Error handling

- Missing Groq API key raises a clear error with setup instructions instead of a raw traceback.
- If a web search returns no results, the pipeline stops gracefully and tells the user, instead of passing empty data downstream to the LLM.

## Example

Input: `what are the latest AI agent frameworks in 2026`

The system retrieves current web results, summarizes them, and returns a clean, structured answer with headings and bullet points.

## Future improvements

- Support for multi-turn conversations with memory
- Basic input validation for nonsensical queries
- Deploy the Streamlit app to a public URL (e.g. Streamlit Community Cloud)
