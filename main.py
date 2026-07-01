import os
from dotenv import load_dotenv
from ddgs import DDGS
from groq import Groq
from typing import TypedDict
from langgraph.graph import StateGraph, END

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Shared state that flows between agents
class AgentState(TypedDict):
    query: str
    raw_results: str
    summary: str
    final_response: str

# Agent 1: Retrieval
def retrieval_agent(state: AgentState) -> AgentState:
    results = DDGS().text(state["query"], max_results=5)
    state["raw_results"] = "\n".join(r["body"] for r in results)
    return state

# Agent 2: Summarizer
def summarizer_agent(state: AgentState) -> AgentState:
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": f"Summarize the key points from this text in 3-5 bullet points:\n\n{state['raw_results']}"}
        ]
    )
    state["summary"] = response.choices[0].message.content
    return state

# Agent 3: Response Generator
def response_agent(state: AgentState) -> AgentState:
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": f"Based on this summary, write a clear, well-formatted answer to the user's question.\n\nQuestion: {state['query']}\n\nSummary:\n{state['summary']}"}
        ]
    )
    state["final_response"] = response.choices[0].message.content
    return state

# Build the graph
graph = StateGraph(AgentState)
graph.add_node("retrieve", retrieval_agent)
graph.add_node("summarize", summarizer_agent)
graph.add_node("respond", response_agent)

graph.set_entry_point("retrieve")
graph.add_edge("retrieve", "summarize")
graph.add_edge("summarize", "respond")
graph.add_edge("respond", END)

app = graph.compile()

if __name__ == "__main__":
    query = input("Enter your research question: ")
    result = app.invoke({"query": query})
    print("\n=== FINAL RESPONSE ===")
    print(result["final_response"])