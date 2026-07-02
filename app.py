import streamlit as st
from main import retrieval_agent, summarizer_agent, response_agent

st.set_page_config(page_title="Research Assistant", page_icon=None, layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background-color: #1c1917;
    background-image:
        radial-gradient(circle at 15% 10%, rgba(251,146,60,0.08) 0%, transparent 40%),
        radial-gradient(circle at 85% 0%, rgba(16,185,129,0.05) 0%, transparent 40%);
}

.stApp, .stApp p, .stApp li, .stApp span, .stApp div,
.stMarkdown, .stMarkdown p, .stMarkdown li,
[data-testid="stMarkdownContainer"], [data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li {
    color: #e7e5e4;
}

.block-container {
    padding-top: 3.5rem !important;
    padding-bottom: 3rem !important;
    max-width: 680px !important;
}

.mono-tag {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    color: #6ee7b7 !important;
    background: rgba(16,185,129,0.08);
    border: 1px solid rgba(16,185,129,0.25);
    padding: 0.35rem 0.8rem;
    border-radius: 6px;
    margin-bottom: 1.6rem;
}
.mono-tag .dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #34d399;
    box-shadow: 0 0 8px #34d399;
}

.headline {
    font-size: 2.3rem;
    font-weight: 800;
    color: #faf9f7 !important;
    line-height: 1.18;
    margin-bottom: 0.9rem;
    letter-spacing: -0.02em;
}
.headline .accent {
    color: #fb923c !important;
}

.subhead {
    font-size: 0.98rem;
    color: #a8a29e !important;
    line-height: 1.6;
    margin-bottom: 1.4rem;
    max-width: 520px;
}

.personal-note {
    font-size: 0.88rem;
    color: #857f79 !important;
    line-height: 1.6;
    margin-bottom: 2.2rem;
    max-width: 520px;
    font-style: italic;
}

.pipeline {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    color: #78716c !important;
    margin-bottom: 2rem;
    letter-spacing: 0.01em;
}
.pipeline span {
    color: #fb923c !important;
}

div[data-testid="stTextInput"] input {
    background-color: #292524;
    border: 1px solid #3f3a37;
    border-radius: 8px;
    padding: 0.8rem 1rem;
    font-size: 0.95rem;
    color: #faf9f7 !important;
}
div[data-testid="stTextInput"] input::placeholder {
    color: #78716c !important;
}
div[data-testid="stTextInput"] input:focus {
    border-color: #fb923c;
    box-shadow: 0 0 0 3px rgba(251,146,60,0.15);
}

div[data-testid="stFormSubmitButton"] button {
    background-color: #ea580c;
    color: white !important;
    border-radius: 8px;
    border: none;
    font-weight: 600;
    font-size: 0.95rem;
    padding: 0.7rem 0;
    margin-top: 0.7rem;
    transition: background-color 0.15s ease;
}
div[data-testid="stFormSubmitButton"] button:hover {
    background-color: #c2410c;
    color: white !important;
}
div[data-testid="stFormSubmitButton"] button p {
    color: white !important;
}

.answer-block {
    margin-top: 2.4rem;
    padding: 1.8rem 1.9rem;
    background: #221f1d;
    border: 1px solid #3a3532;
    border-radius: 12px;
}
.answer-block h3 {
    font-size: 1rem;
    font-weight: 700;
    color: #faf9f7 !important;
    margin-top: 1.3rem;
    margin-bottom: 0.5rem;
    padding-left: 0.7rem;
    border-left: 2px solid #fb923c;
}
.answer-block p, .answer-block li {
    font-size: 0.95rem;
    line-height: 1.65;
    color: #d6d3d1 !important;
}
.answer-block strong {
    color: #faf9f7 !important;
}

.source-snippet {
    background:#292524;
    border:1px solid #3a3532;
    border-radius:8px;
    padding:0.7rem 0.9rem;
    margin-bottom:0.5rem;
    font-size:0.85rem;
    color:#b5b0ac !important;
}
.source-label {
    font-family: 'JetBrains Mono', monospace;
    color:#8a8580 !important;
    font-weight:500;
    font-size: 0.72rem;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}

.footer-note {
    margin-top: 3.5rem;
    font-size: 0.82rem;
    color: #78716c !important;
    text-align: center;
    line-height: 1.5;
}

div[data-testid="stExpander"] {
    background-color: #1f1c1a;
    border: 1px solid #3a3532;
    border-radius: 10px;
}
div[data-testid="stExpander"] summary {
    color: #e7e5e4 !important;
}
</style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.markdown('<div class="mono-tag"><span class="dot"></span>3 agents online</div>', unsafe_allow_html=True)
st.markdown('<div class="headline">Ask anything.<br>Get a <span class="accent">researched</span> answer.</div>', unsafe_allow_html=True)
st.markdown('<div class="subhead">A small pipeline of specialized agents — retrieval, summarization, and response generation — collaborate to turn your question into a clear, sourced answer.</div>', unsafe_allow_html=True)
st.markdown('<div class="personal-note">I built this to actually understand how multi-agent systems work, not just talk about them.</div>', unsafe_allow_html=True)
st.markdown('<div class="pipeline">retrieval_agent <span>&rarr;</span> summarizer_agent <span>&rarr;</span> response_agent</div>', unsafe_allow_html=True)

# ---------- Input ----------
with st.form(key="research_form"):
    query = st.text_input(
        "Research question",
        placeholder="What are the latest AI agent frameworks in 2026?",
        label_visibility="collapsed"
    )
    run_clicked = st.form_submit_button("Research", use_container_width=True)

def escape_dollars(text):
    return text.replace("$", "\\$")

def fix_bullets(text):
    return text.replace("•", "\n- ")

if run_clicked:
    if not query.strip():
        st.warning("Please enter a question first.")
    else:
        state = {"query": query}
        try:
            with st.spinner("Searching the web..."):
                state = retrieval_agent(state)
            with st.spinner("Summarizing findings..."):
                state = summarizer_agent(state)
            with st.spinner("Writing final answer..."):
                state = response_agent(state)
        except Exception as e:
            st.error(f"Something went wrong: {e}")
            st.stop()

        import markdown as md_lib
        final_html = md_lib.markdown(fix_bullets(escape_dollars(state["final_response"])))
        st.markdown(f'<div class="answer-block">{final_html}</div>', unsafe_allow_html=True)

        with st.expander("See how the agents got here"):
            st.markdown('<div class="source-label">Summary — agent 2 output</div>', unsafe_allow_html=True)
            st.markdown(fix_bullets(escape_dollars(state["summary"])))

            st.markdown('<div class="source-label" style="margin-top:1.2rem;">Raw search snippets — agent 1 output</div>', unsafe_allow_html=True)
            snippets = [s.strip() for s in state["raw_results"].split("\n") if s.strip()]
            for i, snippet in enumerate(snippets, start=1):
                snippet = escape_dollars(snippet)
                st.markdown(f"""
                <div class="source-snippet">
                    <span class="source-label">Source {i}</span><br>{snippet}
                </div>
                """, unsafe_allow_html=True)

st.markdown('<div class="footer-note">A small side project exploring how multi-agent AI pipelines actually work.</div>', unsafe_allow_html=True)