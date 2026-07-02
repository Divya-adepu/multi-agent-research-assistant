import os
from dotenv import load_dotenv
from ddgs import DDGS
from groq import Groq
from typing import TypedDict
from langgraph.graph import StateGraph, END

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError(
        "GROQ_API_KEY not found. Create a .env file in the project root with:\n"
        "GROQ_API_KEY=your_key_here\n"
        "Get a free key at https://console.groq.com"
    )

client = Groq(api_key=api_key)

class AgentState(TypedDict):
    query: str
    raw_results: str
    summary: str
    final_response: str

def retrieval_agent(state: AgentState) -> AgentState:
    try:
        results = DDGS().text(state["query"], max_results=5)
    except Exception:
        results = []

    if not results:
        state["raw_results"] = "No search results were found for this query."
    else:
        state["raw_results"] = "\n".join(r["body"] for r in results)
    return state

def summarizer_agent(state: AgentState) -> AgentState:
    if state["raw_results"] == "No search results were found for this query.":
        state["summary"] = "No information was found to summarize."
        return state

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": (
                "Summarize the key points from this text in 3-5 short bullet points. "
                "Each bullet must be on its own new line, starting with a dash '- '. "
                "One clear sentence per bullet. No preamble, no intro sentence, no numbering.\n\n"
                f"{state['raw_results']}"
            )}
        ]
    )
    state["summary"] = response.choices[0].message.content
    return state

def response_agent(state: AgentState) -> AgentState:
    if state["summary"] == "No information was found to summarize.":
        state["final_response"] = (
            "I couldn't find reliable information to answer this question. "
            "Try rephrasing it or being more specific."
        )
        return state

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": (
                "You are writing a final research answer for a user, formatted in clean Markdown.\n"
                "Rules:\n"
                "- Start with a one-sentence direct answer (no heading needed for this part).\n"
                "- Then add 2-4 short sections, each with a '### Heading' and 2-4 concise bullet points.\n"
                "- Do not repeat the question. Do not add a conclusion paragraph. Do not add disclaimers.\n"
                "- Keep the whole thing tight and skimmable, no long paragraphs.\n\n"
                f"Question: {state['query']}\n\n"
                f"Research summary:\n{state['summary']}"
            )}
        ]
    )
    state["final_response"] = response.choices[0].message.content
    return state

def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("retrieve", retrieval_agent)
    graph.add_node("summarize", summarizer_agent)
    graph.add_node("respond", response_agent)

    graph.set_entry_point("retrieve")
    graph.add_edge("retrieve", "summarize")
    graph.add_edge("summarize", "respond")
    graph.add_edge("respond", END)

    return graph.compile()

app = build_graph()

if __name__ == "__main__":
    query = input("Enter your research question: ")
    result = app.invoke({"query": query})
    print("\n=== FINAL RESPONSE ===")
    print(result["final_response"])